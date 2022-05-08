# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    booking_status = models.CharField(max_length=25, default='Available')
    booking_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_room = models.ForeignKey('Room', on_delete=models.CASCADE)
    booking_comment = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['date', 'start_time', 'booking_room']]

    def __str__(self):
        return f"{self.booking_room.room_name} {self.date.strftime('%d/%m/%Y')} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=20, unique=True)
    session_duration = models.IntegerField()
    room_status = models.CharField(max_length=20, default='Available')
    room_comment = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_name
