#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name='ticket_type')
def cut(value):
    if value == 'ADU':
        return 'Người lớn'
    elif value == 'CHI':
        return 'Trẻ em'
    elif value == 'SEN':
        return 'Sơ sinh'
