# Generated by Django 2.2.10 on 2020-05-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NEMO', '0017_remove_facility_and_site_names_from_help_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='count_staff_in_occupancy',
            field=models.BooleanField(default=True, help_text='Indicates that staff users will count towards maximum capacity.'),
        ),
    ]
