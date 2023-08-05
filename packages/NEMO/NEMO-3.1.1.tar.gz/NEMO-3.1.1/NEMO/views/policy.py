from datetime import timedelta, date
from typing import Optional, List

from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Template, Context
from django.utils import timezone

from NEMO.exceptions import InactiveUserError, NoActiveProjectsForUserError, PhysicalAccessExpiredUserError, \
	NoPhysicalAccessUserError, NoAccessiblePhysicalAccessUserError, UnavailableResourcesUserError, \
	MaximumCapacityReachedError, ReservationRequiredUserError, ScheduledOutageInProgressError
from NEMO.models import Reservation, AreaAccessRecord, ScheduledOutage, User, Area, PhysicalAccessLevel, ReservationItemType, Tool, Project
from NEMO.utilities import format_datetime, send_mail
from NEMO.views.customization import get_customization, get_media_file_contents


def check_policy_to_enable_tool(tool: Tool, operator: User, user: User, project: Project, staff_charge: bool):
	"""
	Check that the user is allowed to enable the tool. Enable the tool if the policy checks pass.
	"""
	facility_name = get_customization('facility_name')

	# The tool must be visible (or the parent if it's a child tool) to users.
	visible = tool.parent_tool.visible if tool.is_child_tool() else tool.visible
	if not visible:
		return HttpResponseBadRequest("This tool is currently hidden from users.")

	# The tool must be operational.
	# If the tool is non-operational then it may only be accessed by staff members.
	if not tool.operational and not operator.is_staff:
		return HttpResponseBadRequest("This tool is currently non-operational.")

	# The tool must not be in use.
	current_usage_event = tool.get_current_usage_event()
	if current_usage_event:
		return HttpResponseBadRequest("The tool is currently being used by " + str(current_usage_event.user) + ".")

	# The user must be qualified to use the tool itself, or the parent tool in case of alternate tool.
	tool_to_check_qualifications = tool.parent_tool if tool.is_child_tool() else tool
	if tool_to_check_qualifications not in operator.qualifications.all() and not operator.is_staff:
		return HttpResponseBadRequest("You are not qualified to use this tool.")

	# Only staff members can operate a tool on behalf of another user.
	if (user and operator.pk != user.pk) and not operator.is_staff:
		return HttpResponseBadRequest("You must be a staff member to use a tool on another user's behalf.")

	# All required resources must be available to operate a tool except for staff.
	if tool.required_resource_set.filter(available=False).exists() and not operator.is_staff:
		return HttpResponseBadRequest("A resource that is required to operate this tool is unavailable.")

	# The tool operator may not activate tools in a particular area unless they are logged in to the area.
	# Staff are exempt from this rule.
	if tool.requires_area_access and AreaAccessRecord.objects.filter(area=tool.requires_area_access, customer=operator, staff_charge=None, end=None).count() == 0 and not operator.is_staff:
		dictionary = {
			'operator': operator,
			'tool': tool,
			'type': 'access'
		}
		abuse_email_address = get_customization('abuse_email_address')
		message = get_media_file_contents('unauthorized_tool_access_email.html')
		if abuse_email_address and message:
			rendered_message = Template(message).render(Context(dictionary))
			send_mail("Area access requirement", rendered_message, abuse_email_address, [abuse_email_address])
		return HttpResponseBadRequest("You must be logged in to the {} to operate this tool.".format(tool.requires_area_access.name))

	# The tool operator may not activate tools in a particular area unless they are still within that area reservation window
	if not operator.is_staff and tool.requires_area_reservation():
		if not tool.requires_area_access.get_current_reservation_for_user(operator):
			dictionary = {
				'operator': operator,
				'tool': tool,
				'type': 'reservation',
			}
			abuse_email_address = get_customization('abuse_email_address')
			message = get_media_file_contents('unauthorized_tool_access_email.html')
			if abuse_email_address and message:
				rendered_message = Template(message).render(Context(dictionary))
				send_mail("Area reservation requirement", rendered_message, abuse_email_address, [abuse_email_address])
			return HttpResponseBadRequest("You must have a current reservation for the {} to operate this tool.".format(tool.requires_area_access.name))

	# Staff may only charge staff time for one user at a time.
	if staff_charge and operator.charging_staff_time():
		return HttpResponseBadRequest('You are already charging staff time. You must end the current staff charge before you being another.')

	# Staff may not bill staff time to the themselves.
	if staff_charge and operator == user:
		return HttpResponseBadRequest('You cannot charge staff time to yourself.')

	# Users may only charge to projects they are members of.
	if project not in user.active_projects():
		return HttpResponseBadRequest('The designated user is not assigned to the selected project.')

	# The tool operator must not have a lock on usage
	if operator.training_required:
		return HttpResponseBadRequest(f"You are blocked from using all tools in the {facility_name}. Please complete the {facility_name} rules tutorial in order to use tools.")

	# Users may only use a tool when delayed logoff is not in effect. Staff are exempt from this rule.
	if tool.delayed_logoff_in_progress() and not operator.is_staff:
		return HttpResponseBadRequest("Delayed tool logoff is in effect. You must wait for the delayed logoff to expire before you can use the tool.")

	# Users may not enable a tool during a scheduled outage. Staff are exempt from this rule.
	if tool.scheduled_outage_in_progress() and not operator.is_staff:
		return HttpResponseBadRequest("A scheduled outage is in effect. You must wait for the outage to end before you can use the tool.")

	return HttpResponse()


def check_policy_to_disable_tool(tool, operator, downtime):
	""" Check that the user is allowed to disable the tool. """
	current_usage_event = tool.get_current_usage_event()
	if current_usage_event.operator != operator and current_usage_event.user != operator and not operator.is_staff:
		return HttpResponseBadRequest('You may not disable a tool while another user is using it unless you are a staff member.')
	if downtime < timedelta():
		return HttpResponseBadRequest('Downtime cannot be negative.')
	if downtime > timedelta(minutes=120):
		return HttpResponseBadRequest('Post-usage tool downtime may not exceed 120 minutes.')
	if tool.delayed_logoff_in_progress() and downtime > timedelta():
		return HttpResponseBadRequest('The tool is already in a delayed-logoff state. You may not issue additional delayed logoffs until the existing one expires.')
	if not tool.allow_delayed_logoff and downtime > timedelta():
		return HttpResponseBadRequest('Delayed logoff is not allowed for this tool.')
	return HttpResponse()


def check_policy_to_save_reservation(cancelled_reservation: Optional[Reservation], new_reservation: Reservation, user_creating_reservation: User, explicit_policy_override: bool):
	"""
		Check the reservation creation policy and return a list of policy problems if any.
	"""
	user = new_reservation.user

	facility_name = get_customization('facility_name')

	# The function will check all policies. Policy problems are placed in the policy_problems list. overridable is True if the policy problems can be overridden by a staff member.
	policy_problems = []
	overridable = False

	item_type = new_reservation.reservation_item_type

	# Reservations may not have a start time that is earlier than the end time.
	if new_reservation.start >= new_reservation.end:
		policy_problems.append("Reservation start time (" + format_datetime(new_reservation.start) + ") must be before the end time (" + format_datetime(new_reservation.end) + ").")

	check_coincident_item_reservation_policy(cancelled_reservation, new_reservation, user_creating_reservation, policy_problems)

	# Reservations that have been cancelled may not be changed.
	if new_reservation.cancelled:
		policy_problems.append("This reservation has already been cancelled by " + str(new_reservation.cancelled_by) + " at " + format_datetime(new_reservation.cancellation_time) + ".")

	# The user must belong to at least one active project to make a reservation.
	if user.active_project_count() < 1:
		if user == user_creating_reservation:
			policy_problems.append("You do not belong to any active projects. Thus, you may not create any reservations.")
		else:
			policy_problems.append(str(user) + " does not belong to any active projects and cannot have reservations.")

	# The user must associate their reservation with a project they belong to.
	if new_reservation.project and new_reservation.project not in user.active_projects():
		if user == user_creating_reservation:
			policy_problems.append("You do not belong to the project associated with this reservation.")
		else:
			policy_problems.append(str(user) + " does not belong to the project named " + str(new_reservation.project) + ".")

	# If the user is a staff member or there's an explicit policy override then the policy check is finished.
	if user.is_staff or explicit_policy_override:
		return policy_problems, overridable

	# If there are no blocking policy conflicts at this point, the rest of the policies can be overridden.
	if not policy_problems:
		overridable = True

	# Some tool reservations require a prior area reservation
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if item_type == ReservationItemType.TOOL:
		if new_reservation.tool.requires_area_reservation():
			area: Area = new_reservation.tool.requires_area_access
			# Check that a reservation for the area has been made and contains the start time
			if not Reservation.objects.filter(missed=False, cancelled=False, shortened=False,
											  user=user, area=area,
											  start__lte=new_reservation.start,
											  end__gt=new_reservation.start).exists():
				if user == user_creating_reservation:
					policy_problems.append(f"This tool requires a {area} reservation. Please make a reservation in the {area} prior to reserving this tool.")
				else:
					policy_problems.append(f"This tool requires a {area} reservation. Please make sure to also create a reservation in the {area} or {str(user)} will not be able to enter the area.")

	# The user must complete training to create reservations.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if user.training_required:
		if user == user_creating_reservation:
			policy_problems.append(f"You are blocked from making reservations in the {facility_name}. Please complete the {facility_name} rules tutorial in order to create new reservations.")
		else:
			policy_problems.append(f"{str(user)} is blocked from making reservations in the {facility_name}. The user needs to complete the {facility_name} rules tutorial in order to create new reservations.")

	# Users may only change their own reservations.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if cancelled_reservation and user != user_creating_reservation:
		policy_problems.append("You may not change reservations that you do not own.")

	# The user may not create or move a reservation to have a start time that is earlier than the current time.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if new_reservation.start < timezone.now():
		policy_problems.append("Reservation start time (" + format_datetime(new_reservation.start) + ") is earlier than the current time (" + format_datetime(timezone.now()) + ").")

	# The user may not move or resize a reservation to have an end time that is earlier than the current time.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if new_reservation.end < timezone.now():
		policy_problems.append("Reservation end time (" + format_datetime(new_reservation.end) + ") is earlier than the current time (" + format_datetime(timezone.now()) + ").")

	# The user must be qualified on the tool in question in order to create, move, or resize a reservation.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if new_reservation.tool and new_reservation.tool not in user.qualifications.all():
		if user == user_creating_reservation:
			policy_problems.append("You are not qualified to use this tool. Creating, moving, and resizing reservations is forbidden.")
		else:
			policy_problems.append(f"{str(user)} is not qualified to use this tool. Creating, moving, and resizing reservations is forbidden.")

	# The user must be authorized on the area in question at the start and end times of the reservation in order to create, move, or resize a reservation.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if item_type == ReservationItemType.AREA:
		user_access_levels = user.accessible_access_levels_for_area(new_reservation.area)
		if not any([access_level.accessible_at(new_reservation.start) for access_level in user_access_levels]) or not any([access_level.accessible_at(new_reservation.end) for access_level in user_access_levels]):
			details = f" (times allowed in this area are: {','.join([access.get_schedule_display_with_times() for access in user_access_levels])})" if user_access_levels else ''
			if user == user_creating_reservation:
				policy_problems.append(f"You are not authorized to access this area at this time{details}. Creating, moving, and resizing reservations is forbidden.")
			else:
				policy_problems.append(f"{str(user)} is not authorized to access this area at this time{details}. Creating, moving, and resizing reservations is forbidden.")

	# The reservation start time may not exceed the item's reservation horizon.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	item = new_reservation.reservation_item
	if item.reservation_horizon is not None:
		reservation_horizon = timedelta(days=item.reservation_horizon)
		if new_reservation.start > timezone.now() + reservation_horizon:
			policy_problems.append("You may not create reservations further than " + str(reservation_horizon.days) + f" days from now for this {item_type.value}.")

	# Check item policy rules
	item_policy_problems = []
	if should_enforce_policy(new_reservation):
		item_policy_problems = check_policy_rules_for_item(cancelled_reservation, new_reservation, user_creating_reservation)

	# Return the list of all policies that are not met.
	return policy_problems + item_policy_problems, overridable


def check_coincident_item_reservation_policy(cancelled_reservation: Optional[Reservation], new_reservation: Reservation, user_creating_reservation: User, policy_problems: List):
	user = new_reservation.user

	# For tools the user may not create, move, or resize a reservation to coincide with another user's reservation.
	# For areas, it cannot coincide with another reservation for the same user, or with a number of other users greater than the area capacity
	coincident_events = Reservation.objects.filter(cancelled=False, missed=False, shortened=False)
	# Exclude the reservation we're cancelling in order to create a new one:
	if cancelled_reservation and cancelled_reservation.id:
		coincident_events = coincident_events.exclude(id=cancelled_reservation.id)
	# Exclude events for which the following is true:
	# The event starts and ends before the time-window, and...
	# The event starts and ends after the time-window.
	coincident_events = coincident_events.exclude(start__lt=new_reservation.start, end__lte=new_reservation.start)
	coincident_events = coincident_events.exclude(start__gte=new_reservation.end, end__gt=new_reservation.end)
	if new_reservation.reservation_item_type == ReservationItemType.TOOL and coincident_events.filter(**new_reservation.reservation_item_filter).count() > 0:
		policy_problems.append("Your reservation coincides with another reservation that already exists. Please choose a different time.")
	if new_reservation.reservation_item_type == ReservationItemType.AREA:
		if coincident_events.filter(**new_reservation.reservation_item_filter).filter(user=user).count() > 0:
			if user == user_creating_reservation:
				policy_problems.append("You already have a reservation that coincides with this one. Please choose a different time.")
			else:
				policy_problems.append(f"{str(user)} already has a reservation that coincides with this one. Please choose a different time.")
		for area in new_reservation.area.get_ancestors(ascending=True, include_self=True):
			# Check reservations for all other children of the parent areas
			apply_to_user = not user.is_staff or user.is_staff and area.count_staff_in_occupancy
			children_events = coincident_events.filter(area_id__in=[area.id for area in area.get_descendants(include_self=True)])
			# Check only distinct users since the same user could make reservations in different rooms
			distinct_users = set(children_events.values_list('user', flat=True).distinct())
			distinct_users.add(user.id)
			if apply_to_user and area.maximum_capacity and len(distinct_users) > area.maximum_capacity:
				policy_problems.append(f"The {area} is already at its maximum capacity at this time. Please choose a different time.")

	# The user may not create, move, or resize a reservation to coincide with a scheduled outage.
	if new_reservation.reservation_item_type == ReservationItemType.TOOL:
		coincident_events = ScheduledOutage.objects.filter(
			Q(tool=new_reservation.tool) | Q(resource__fully_dependent_tools__in=[new_reservation.tool]))
	elif new_reservation.reservation_item_type == ReservationItemType.AREA:
		coincident_events = new_reservation.area.scheduled_outage_queryset()
	# Exclude events for which the following is true:
	# The event starts and ends before the time-window, and...
	# The event starts and ends after the time-window.
	coincident_events = coincident_events.exclude(start__lt=new_reservation.start, end__lte=new_reservation.start)
	coincident_events = coincident_events.exclude(start__gte=new_reservation.end, end__gt=new_reservation.end)
	if coincident_events.count() > 0:
		policy_problems.append("Your reservation coincides with a scheduled outage. Please choose a different time.")


def should_enforce_policy(reservation: Reservation):
	""" Returns whether or not the policy rules should be enforced. """
	should_enforce = True

	item = reservation.reservation_item
	start_time = timezone.localtime(reservation.start)
	end_time = timezone.localtime(reservation.end)
	if item.policy_off_weekend and start_time.weekday() >= 5 and end_time.weekday() >= 5:
		should_enforce = False
	if item.policy_off_between_times and item.policy_off_start_time and item.policy_off_end_time:
		if item.policy_off_start_time <= item.policy_off_end_time:
			""" Range is something like 6am-6pm """
			if item.policy_off_start_time <= start_time.time() <= item.policy_off_end_time and item.policy_off_start_time <= end_time.time() <= item.policy_off_end_time:
				should_enforce = False
		else:
			""" Range is something like 6pm-6am """
			if (item.policy_off_start_time <= start_time.time() or start_time.time() <= item.policy_off_end_time) and (item.policy_off_start_time <= end_time.time() or end_time.time() <= item.policy_off_end_time):
				should_enforce = False
	return should_enforce


def check_policy_rules_for_item(cancelled_reservation: Optional[Reservation], new_reservation: Reservation, user_creating_reservation: User):
	item_policy_problems = []
	# Calculate the duration of the reservation:
	duration = new_reservation.end - new_reservation.start

	# The reservation must be at least as long as the minimum block time for this item.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	item = new_reservation.reservation_item
	item_type = new_reservation.reservation_item_type
	if item.minimum_usage_block_time:
		minimum_block_time = timedelta(minutes=item.minimum_usage_block_time)
		if duration < minimum_block_time:
			item_policy_problems.append(f"Your reservation has a duration of {str(int(duration.total_seconds() / 60))} minutes. This {item_type.value} requires a minimum reservation duration of {str(int(minimum_block_time.total_seconds() / 60))} minutes.")

	# The reservation may not exceed the maximum block time for this tool.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if item.maximum_usage_block_time:
		maximum_block_time = timedelta(minutes=item.maximum_usage_block_time)
		if duration > maximum_block_time:
			item_policy_problems.append(f"Your reservation has a duration of {str(int(duration.total_seconds() / 60))} minutes. Reservations for this {item_type.value} may not exceed {str(int(maximum_block_time.total_seconds() / 60))} minutes.")

	user = new_reservation.user

	# If there is a limit on number of reservations per user per day then verify that the user has not exceeded it.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if item.maximum_reservations_per_day:
		start_of_day = new_reservation.start
		start_of_day = start_of_day.replace(hour=0, minute=0, second=0, microsecond=0)
		end_of_day = start_of_day + timedelta(days=1)
		reservations_for_that_day = Reservation.objects.filter(cancelled=False, shortened=False, start__gte=start_of_day, end__lte=end_of_day, user=user)
		reservations_for_that_day = reservations_for_that_day.filter(**new_reservation.reservation_item_filter)
		# Exclude any reservation that is being cancelled.
		if cancelled_reservation and cancelled_reservation.id:
			reservations_for_that_day = reservations_for_that_day.exclude(id=cancelled_reservation.id)
		if reservations_for_that_day.count() >= item.maximum_reservations_per_day:
			if user == user_creating_reservation:
				item_policy_problems.append(f"You may only have {str(item.maximum_reservations_per_day)} reservations for this {item_type.value} per day. Missed reservations are included when counting the number of reservations per day.")
			else:
				item_policy_problems.append(f"{str(user)} may only have {str(item.maximum_reservations_per_day)} reservations for this {item_type.value} per day. Missed reservations are included when counting the number of reservations per day.")

	# A minimum amount of time between reservations for the same user & same tool can be enforced.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if item.minimum_time_between_reservations:
		buffer_time = timedelta(minutes=item.minimum_time_between_reservations)
		must_end_before = new_reservation.start - buffer_time
		too_close = Reservation.objects.filter(cancelled=False, shortened=False, user=user, end__gt=must_end_before, start__lt=new_reservation.start)
		too_close = too_close.filter(**new_reservation.reservation_item_filter)
		if cancelled_reservation and cancelled_reservation.id:
			too_close = too_close.exclude(id=cancelled_reservation.id)
		if too_close.exists():
			if user == user_creating_reservation:
				item_policy_problems.append(f"Separate reservations for this {item_type.value} that belong to you must be at least {str(item.minimum_time_between_reservations)} minutes apart from each other. The proposed reservation ends too close to another reservation.")
			else:
				item_policy_problems.append(f"Separate reservations for this {item_type.value} that belong to {str(user)} must be at least {str(item.minimum_time_between_reservations)} minutes apart from each other. The proposed reservation ends too close to another reservation.")
		must_start_after = new_reservation.end + buffer_time
		too_close = Reservation.objects.filter(cancelled=False, shortened=False, user=user, start__lt=must_start_after, end__gt=new_reservation.start)
		too_close = too_close.filter(**new_reservation.reservation_item_filter)
		if cancelled_reservation and cancelled_reservation.id:
			too_close = too_close.exclude(id=cancelled_reservation.id)
		if too_close.exists():
			if user == user_creating_reservation:
				item_policy_problems.append(f"Separate reservations for this {item_type.value} that belong to you must be at least {str(item.minimum_time_between_reservations)} minutes apart from each other. The proposed reservation begins too close to another reservation.")
			else:
				item_policy_problems.append(f"Separate reservations for this {item_type.value} that belong to {str(user)} must be at least {str(item.minimum_time_between_reservations)} minutes apart from each other. The proposed reservation begins too close to another reservation.")

	# Check that the user is not exceeding the maximum amount of time they may reserve in the future.
	# Staff may break this rule.
	# An explicit policy override allows this rule to be broken.
	if item.maximum_future_reservation_time:
		reservations_after_now = Reservation.objects.filter(cancelled=False, user=user, start__gte=timezone.now())
		reservations_after_now = reservations_after_now.filter(**new_reservation.reservation_item_filter)
		if cancelled_reservation and cancelled_reservation.id:
			reservations_after_now = reservations_after_now.exclude(id=cancelled_reservation.id)
		amount_reserved_in_the_future = new_reservation.duration()
		for r in reservations_after_now:
			amount_reserved_in_the_future += r.duration()
		if amount_reserved_in_the_future.total_seconds() / 60 > item.maximum_future_reservation_time:
			if user == user_creating_reservation:
				item_policy_problems.append(f"You may only reserve up to {str(item.maximum_future_reservation_time)} minutes of time on this {item_type.value}, starting from the current time onward.")
			else:
				item_policy_problems.append(f"{str(user)} may only reserve up to {str(item.maximum_future_reservation_time)} minutes of time on this {item_type.value}, starting from the current time onward.")

	return item_policy_problems


def check_policy_to_cancel_reservation(reservation, user_cancelling_reservation):
	"""
	Checks the reservation deletion policy.
	If all checks pass the function returns an HTTP "OK" response.
	Otherwise, the function returns an HTTP "Bad Request" with an error message.
	"""

	# Users may only cancel reservations that they own.
	# Staff may break this rule.
	if (reservation.user != user_cancelling_reservation) and not user_cancelling_reservation.is_staff:
		return HttpResponseBadRequest("You may not cancel reservations that you do not own.")

	# Users may not cancel reservations that have already ended.
	# Staff may break this rule.
	if reservation.end < timezone.now() and not user_cancelling_reservation.is_staff:
		return HttpResponseBadRequest("You may not cancel reservations that have already ended.")

	if reservation.cancelled:
		return HttpResponseBadRequest("This reservation has already been cancelled by " + str(reservation.cancelled_by) + " at " + format_datetime(reservation.cancellation_time) + ".")

	if reservation.missed:
		return HttpResponseBadRequest("This reservation was missed and cannot be modified.")

	return HttpResponse()


def check_policy_to_create_outage(outage: ScheduledOutage):
	# Outages may not have a start time that is earlier than the end time.
	if outage.start >= outage.end:
		return "Outage start time (" + format_datetime(outage.start) + ") must be before the end time (" + format_datetime(outage.end) + ")."

	# The user may not create, move, or resize an outage to coincide with another user's reservation.
	coincident_events = Reservation.objects.filter(**outage.outage_item_filter).filter(cancelled=False, missed=False, shortened=False)
	# Exclude events for which the following is true:
	# The event starts and ends before the time-window, and...
	# The event starts and ends after the time-window.
	coincident_events = coincident_events.exclude(start__lt=outage.start, end__lte=outage.start)
	coincident_events = coincident_events.exclude(start__gte=outage.end, end__gt=outage.end)
	if coincident_events.count() > 0:
		return "Your scheduled outage coincides with a reservation that already exists. Please choose a different time."

	# No policy issues! The outage can be created...
	return None


def check_policy_to_enter_any_area(user: User):
	"""
	Checks the area access policy for a user.
	"""
	if not user.is_active:
		raise InactiveUserError(user=user)

	if user.active_project_count() < 1:
		raise NoActiveProjectsForUserError(user=user)

	if user.access_expiration is not None and user.access_expiration < date.today():
		raise PhysicalAccessExpiredUserError(user=user)

	user_has_access_to_at_least_one_area = user.accessible_access_levels().exists()
	if not user_has_access_to_at_least_one_area:
		raise NoPhysicalAccessUserError(user=user)


def check_policy_to_enter_this_area(area:Area, user:User):
	# If explicitly set on the Physical Access Level, staff may be exempt from being granted explicit access
	if user.is_staff and any([access_level.accessible() for access_level in PhysicalAccessLevel.objects.filter(allow_staff_access=True, area=area)]):
		pass
	else:
		# Check if the user normally has access to this area door at the current time (or access to any parent)
		if not any([access_level.accessible() for access_level in user.accessible_access_levels_for_area(area)]):
			raise NoAccessiblePhysicalAccessUserError(user=user, area=area)

	if not user.is_staff:
		for a in area.get_ancestors(ascending=True, include_self=True):
			unavailable_resources = a.required_resources.filter(available=False)
			if unavailable_resources:
				raise UnavailableResourcesUserError(user=user, area=a, resources=unavailable_resources)

		# Non staff users may not enter an area during a scheduled outage.
		if area.scheduled_outage_in_progress():
			raise ScheduledOutageInProgressError(user=user, area=area)

		# If we reached maximum capacity, fail (only for non staff users)
		for a in area.get_ancestors(ascending=True, include_self=True):
			if a.maximum_capacity and 0 < a.maximum_capacity <= a.occupancy_count():
				raise MaximumCapacityReachedError(user=user, area=a)

		if area.requires_reservation and not area.get_current_reservation_for_user(user):
			raise ReservationRequiredUserError(user=user, area=area)

