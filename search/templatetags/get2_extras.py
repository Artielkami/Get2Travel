#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.db.models.query import QuerySet
import simplejson
from django.utils.safestring import mark_safe
from django.core.serializers import serialize

register = template.Library()


@register.simple_tag(name='price')
def makeprice(quan, pr1, pr2, pr3, ft1, ft2, ft3):
    price = quan['adult']*pr1 + quan['child']*pr2 + quan['babe']*pr3 + \
            ft1 + ft2 + ft3
    return price

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='carrier')
def carrier(value):
    if value == 'jsa':
        return 'JetStar'
    elif value == 'vna':
        return 'VN Airline'
    else:
        return 'VietJet'


@register.filter(name='clat')
def clat(value):
    if value == 'save':
        return 'Siêu tiết kiệm'
    elif value == 'first':
        return 'Hạng nhất'
    elif value == 'business':
        return 'Thương gia'
    elif value == 'economy':
        return 'Phổ thông'
    else:
        return 'Đặc biệt'

@register.filter('jsonify')
def jsonify(object):
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object))
    return mark_safe(simplejson.dumps(object))

@register.filter(name='ticket_type')
def cut(value):
    if value == 'vna_bf':
        return 'Thương gia linh hoạt'
    elif value == 'vna_bs':
        return 'Thương gia tiêu chuẩn'
    elif value == 'vna_ef':
        return 'Phổ thông linh hoạt'
    elif value == 'vna_es':
        return 'Phổ thông tiêu chuẩn'
    elif value == 'vna_esa':
        return 'Phổ thông tiết kiệm'
    elif value == 'vna_sd':
        return 'Siêu tiết kiệm'
    elif value == 'vja_promo':
        return 'Siêu khuyến mãi'
    elif value == 'vja_eco':
        return 'Phổ thông'
    elif value == 'vja_sky':
        return 'Cao cấp'
    elif value == 'jsa_save':
        return 'Tiết kiệm'
    elif value == 'jsa_flex':
        return 'Linh hoạt'
    elif value == 'jsa_opt':
        return 'Tối ưu'
