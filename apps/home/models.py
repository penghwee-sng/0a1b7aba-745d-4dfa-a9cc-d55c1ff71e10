# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.conf import settings
import pytz

# Create your models here.


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    datetime_start = models.DateTimeField(unique=True)
    datetime_end = models.DateTimeField()
    booking_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_room = models.ForeignKey('Room', on_delete=models.CASCADE)
    scenario = models.IntegerField(default=0)
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

        print(start, end)

        # check for items that have an overlapping start date
        booking_overlapping_start = Booking.objects.filter(
            datetime_start__gt=start,
            datetime_start__lt=end,
            booking_room_id=self.booking_room).exists()

        # check for items that have an overlapping end date
        booking_overlapping_end = Booking.objects.filter(
            datetime_end__gt=start, datetime_end__lt=end).exists()

        # check for items that envelope this item
        booking_enveloping = Booking.objects.filter(
            datetime_start__lte=start, datetime_end__gte=end).exists()
        print(booking_overlapping_start,
              booking_overlapping_end, booking_enveloping)

        booking_items_present = booking_overlapping_start or booking_overlapping_end or booking_enveloping

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
    room_status = models.CharField(max_length=20, default='Available')
    room_comment = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_name
