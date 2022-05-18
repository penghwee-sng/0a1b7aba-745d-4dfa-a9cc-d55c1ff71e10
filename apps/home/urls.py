# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('api/<name>/', views.api, name='api'),
    path('api/<name>/<id>', views.api, name='api'),
    
    path('api/blockings/<start_date>/<start_time>/<end_date>/<end_time>/<room_id>', views.get_blocked_bookings, name='api'),

    # Matches any html file
    re_path(r'^.*\.*html', views.pages, name='pages'),

]
