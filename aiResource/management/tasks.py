# -*- coding:utf-8 -*-
from celery import task
from models import Resource


@task
def check():
    all_pid = Resource.objects.filter(pid=0).all()
    for pid in all_pid:
        pid_data_list = Resource.objects.filter(pid=pid.id).order_by("id").all()
        none_count = 0
        for item in pid_data_list:
            if item.value is None:
                none_count += 1
        none_per = 100 - int(float(float(none_count) / float(len(pid_data_list)) * 100))
        ret = Resource.objects.filter(id=pid.id).update(checked=none_per)
