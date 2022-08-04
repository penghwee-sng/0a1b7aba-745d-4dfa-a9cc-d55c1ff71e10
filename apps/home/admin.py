# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Room, Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('datetime_start', 'booking_user', 'booking_room', 'scenario')
    list_filter = ('booking_user',)

# Register your models here.
admin.site.register(Booking, BookingAdmin)
admin.site.register(Room)
admin.site.site_header = 'Training Booking System Administration'
