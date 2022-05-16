# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from .models import Room, Booking
from datetime import datetime, timedelta
from django.core import serializers
from django.contrib.auth import get_user_model


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
    if name == 'rooms':
        if id is None:
            return JsonResponse(list(Room.objects.values()), safe=False)
        else:
            # get all users

            users = list(get_user_model().objects.all().values('id','username'))
            room = list(Room.objects.filter(room_id=id).values())[0]
            booking = list(Booking.objects.select_related('booking_user_id').filter(booking_room_id=id, date__gte=datetime.now(), date__lte=datetime.now()+timedelta(days=28)).values())
            return JsonResponse({
                'room': room, 
                'booking':booking,
                'users':users
            }, safe=False)
    if name == 'bookings':
        if request.method == 'POST':
            data = request.POST
            Booking.objects.create(date=data['date'], start_time=f"{data['time']}:00", end_time=f"{data['endtime']}:00", booking_room_id=data['room_id'], booking_user_id=request.user.id)
            return JsonResponse({'status': 'success'}, safe=False)
        if request.method == 'GET':
            if id is None:
                return JsonResponse(list(Booking.objects.filter(booking_user_id=request.user.id, date__gte=datetime.now()).order_by('date').values()), safe=False)
        if request.method == 'DELETE':
            if id is not None:
                Booking.objects.filter(booking_id=id, booking_user_id=request.user.id).delete()
                return JsonResponse({'status': 'success'}, safe=False)
    return JsonResponse({'name': name})
