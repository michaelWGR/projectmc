# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=512)
    type = models.IntegerField()  # 资源类类型：0：video,1:frame,2:audio
    business_type = models.IntegerField(default=0)  # 业务类型：0：鉴黄，1：AD-OCR 2:GAME-OCR
    value = models.TextField(null=True)
    pid = models.IntegerField()  # 如果没有 pid 则置为0
    next_id = models.IntegerField()  # 如果没有 next_id 则置为0
    pre_id = models.IntegerField()  # 如果没有 pre_id 则置为0
    is_leaf = models.IntegerField()  # 标识是否有后处理 针对帧 视频默认为0
    checked = models.IntegerField(default=0)
    process_type = models.IntegerField()  # 参考aiResource.setting.PROCESS_TYPE
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    remark = models.TextField(null=True)

    """
    type: game_ocr

    col_int_01 -> game_type index
    col_json_01 -> all_info (继承)
    """
    col_int_01 = models.IntegerField(default=0)
    col_json_01 = models.TextField(null=True)
    is_debug = models.IntegerField(default=0)  # id_debug 1: 调试数据 0：正式数据

    class Meta:
        db_table = 'resources'


class PornResult(models.Model):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource, null=False, db_constraint=False, db_index=True)

    product = models.CharField(max_length=16, db_index=True)
    label = models.IntegerField(default=0)
    rate = models.FloatField(default=0.0)
    is_review = models.IntegerField(default=0)
    is_error = models.IntegerField(default=0)
    errors = models.TextField(null=True)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    remark = models.TextField(null=True)

    class Meta:
        db_table = 'porn_results'
        # unique_together = (('resource', 'product'), )


class OCRResult(models.Model):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource, null=False, db_constraint=False, db_index=True)

    product = models.CharField(max_length=16, db_index=True)
    items = models.TextField(null=True)
    is_error = models.IntegerField(default=0)
    errors = models.TextField(null=True)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    remark = models.TextField(null=True)

    class Meta:
        db_table = 'ocr_results'
        # unique_together = (('resource', 'product'), )


class TempReview(models.Model):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(Resource, null=False, db_constraint=False, db_index=True)
    review_status = models.IntegerField(default=0)  # 1: no_need 2: need 3: reviewed
    old_value = models.IntegerField(null=True)
    new_value = models.IntegerField(null=True)
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'temp_reviews'
