# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Room, Booking

# Register your models here.
admin.site.register(Booking)
admin.site.register(Room)
admin.site.site_header = 'Training Booking System Administration'
