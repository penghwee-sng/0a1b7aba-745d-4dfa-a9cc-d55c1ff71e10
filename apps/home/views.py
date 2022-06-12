# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import timedelta
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Room, Booking


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    context['segment'] = 'booking.html'
    html_template = loader.get_template('home/booking.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def api(request, name, id=None):
    if name == 'all':
        return JsonResponse({
            'rooms': list(Room.objects.values()),
            'bookings': list(Booking.objects.filter(datetime_start__gte=timezone.now()-timedelta(days=2)).values()),
            'users': list(get_user_model().objects.all().values('id', 'username'))
        }, safe=False)
    if name == 'rooms':
        if id is None:
            return JsonResponse({
                'rooms': list(Room.objects.values())
            }, safe=False)

        else:
            # get all users

            users = list(
                get_user_model().objects.all().values('id', 'username'))
            room = list(Room.objects.filter(room_id=id).values())[0]
            booking = list(Booking.objects.select_related('booking_user_id').filter(
                booking_room_id=id, datetime_start__gte=timezone.now(), datetime_end__lte=timezone.now()+timedelta(days=28)).values())
            return JsonResponse({
                'room': room,
                'booking': booking,
                'users': users
            }, safe=False)

    if name == 'bookings':
        if request.method == 'POST':
            data = request.POST
            # delete overlapping bookings if is admin
            if request.user.is_superuser:
                Booking.objects.filter(
                    booking_room_id=data['room_id'],
                    datetime_start__gte=data['datetime_start'],
                    datetime_end__lte=data['datetime_end']).delete()

            Booking.objects.create(datetime_start=data['datetime_start'], datetime_end=data['datetime_end'],
                                   booking_room_id=data['room_id'], booking_user_id=request.user.id, scenario=data['scenario'], pax=data['pax'])
            return JsonResponse({'status': 'success'}, safe=False)
        if request.method == 'GET':
            if id is None:
                print(request.user.id)
                return JsonResponse(list(Booking.objects.filter(booking_user_id=request.user.id, datetime_start__gte=timezone.now()-timedelta(days=2)).order_by('datetime_start').values()), safe=False)
        if request.method == 'DELETE':
            if id is not None:
                Booking.objects.filter(
                    booking_id=id, booking_user_id=request.user.id).delete()
                return JsonResponse({'status': 'success'}, safe=False)
    return JsonResponse({'name': name})


def get_blocked_bookings(request, start_date, start_time, end_date, end_time, room_id):
    bookings = Booking.objects.filter(
        date__gte=start_date, date__lte=end_date, booking_room_id=room_id)
    return JsonResponse(list(bookings.values()), safe=False)
