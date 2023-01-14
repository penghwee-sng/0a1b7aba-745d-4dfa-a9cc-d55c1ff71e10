from django.contrib import admin
from .models import Room, Booking, TelegramToUser


class BookingAdmin(admin.ModelAdmin):
    list_display = ("datetime_start", "booking_user", "booking_room", "scenario", "pax")
    list_filter = ("booking_user",)


# Register your models here.
admin.site.register(Booking, BookingAdmin)
admin.site.register(Room)
admin.site.register(TelegramToUser)
admin.site.site_header = "Training Booking System Administration"
