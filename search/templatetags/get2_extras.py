#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.simple_tag(name='price')
def makeprice(quan, pr1, pr2, pr3, ft1, ft2, ft3):
    price = quan['adult']*pr1 + quan['child']*pr2 + quan['babe']*pr3 + \
            ft1 + ft2 + ft3
    return price


@register.filter(name='carrier')
def carrier(value):
    if value == 'pja':
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


@register.filter(name='ticket_type')
def cut(value):
    if value == 'ADU':
        return 'Người lớn'
    elif value == 'CHI':
        return 'Trẻ em'
    elif value == 'SEN':
        return 'Sơ sinh'
