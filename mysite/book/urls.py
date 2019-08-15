# -*- coding: utf-8 -*-
from django.conf.urls import url


from . import views

app_name = 'book'

urlpatterns = [
    url(r'^mypage/$', views.mypage, name='mypage'),
    url(r'^$', views.current_datetime, name='current_datetime'),
    url(r'^plus/(?P<offset>\d{1,2})/$', views.hours_ahead, name='hours_ahead'),
    url(r'^search-form/$', views.search_form, name='search_form'),
    url(r'^search/$', views.search, name='search_form'),
    url(r'^contact/$', views.contact, name='contact'),
]