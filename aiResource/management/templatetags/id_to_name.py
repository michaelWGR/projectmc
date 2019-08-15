# -*_ coding: utf-8 -*-

from django import template

register = template.Library()


@register.filter
def parse_business_type(id):
    id_name_dict = {
        '0': '鉴黄',
        '1': '广告OCR',
        '2': '游戏OCR'
    }

    return id_name_dict.get(str(id))
