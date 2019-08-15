from __future__ import absolute_import

from django.conf.urls import include, url
from django.views.generic import TemplateView

from management import views

urlpatterns = [
    # url(r'^resource$', views.resource_index),
    url(r'^resource$', views.resource_index, name='resource_index'),
    url(r'^list', views.plist),

    url(r'^resource/checker/(?P<resource_id>\d+)$', views.resource_checker),
    url(r'^resource/review/(?P<review_id>\d+)$', views.resource_review),
    url(r'^resource/batch_update_value', views.batch_update_value),
    url(r'^resource/batch_update_json', views.batch_update_json),
    url(r'^resource/review_update', views.review_update)
    # url(r'^resource/index$', views.resource_index),
]
