# Generated by Django 4.0.1 on 2022-05-18 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_booking_end_datetime_booking_start_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='end_datetime',
            new_name='datetime_end',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='start_datetime',
            new_name='datetime_start',
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('datetime_start', 'booking_room')},
        ),
        migrations.RemoveField(
            model_name='booking',
            name='booking_comment',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='booking_status',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='start_time',
        ),
    ]
