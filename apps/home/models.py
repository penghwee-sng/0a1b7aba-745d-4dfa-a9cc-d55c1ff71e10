# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import timedelta
from django.db import models
from django.conf import settings
import pytz

# Create your models here.

# calculate number of working days between two dates
def working_days(start_date, end_date):
    working_days = 0
    for i in range(int((end_date - start_date).days)):
        if start_date.weekday() < 5:
            working_days += 1
        start_date += timedelta(days=1)
    return working_days


class Booking(models.Model):
    list_display('datetime_start', 'booking_user', 'booking_room', 'scenario')
    booking_id = models.AutoField(primary_key=True)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    booking_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_room = models.ForeignKey('Room', on_delete=models.CASCADE)
    scenario = models.IntegerField(default=0)
    pax = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        time_zone = pytz.timezone('Asia/Singapore')
        return f"{self.booking_room.room_name} | {self.datetime_start.astimezone(time_zone).strftime('%d/%m/%Y')} - {self.datetime_end.astimezone(time_zone).strftime('%d/%m/%Y')}"

    # ensure no overlapping bookings before save
    def save(self, *args, **kwargs):
        # YYYY-MM-DD
        start = self.datetime_start
        end = self.datetime_end
        if start >= end:
            raise ValueError('Start time must be before end time')

        # check if user is admin, if so, skip check
        if self.booking_user in (1, 2):
            super(Booking, self).save(*args, **kwargs)

        overlapping_booking_items = Booking.objects.filter(
            datetime_start__lte=end,
            datetime_end__gte=start,
            booking_room_id=self.booking_room)

        booking_items_present = overlapping_booking_items.exists()

        # todo: check minimum number of days required to book

        if booking_items_present:
            raise ValueError('This booking overlaps with another booking')
        else:
            super(Booking, self).save(*args, **kwargs)


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=20, unique=True)
    session_duration = models.IntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    scenarios = models.IntegerField(default=0)
    prep_days = models.IntegerField(default=0)
    room_status = models.CharField(max_length=20, default='Available')
    room_comment = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_name
