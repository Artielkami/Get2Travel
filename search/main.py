#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import Ticket, Carrier, Airport
from django.db.models import F
import random
import datetime


class Main (object):
    """Lõi xử lý chính"""

    @staticmethod
    def get_ticket(dep, arr, go_day, rt_day='xxx', way=1, stop=0, ttype='all'):
        if ttype == 'all':
            return Ticket.objects.filter(departure_port=dep,
                                         arrival_port=arr,
                                         ticket_type=ttype,
                                         departure_time__range=(datetime.datetime.combine(go_day, datetime.time.min),
                                                                datetime.datetime.combine(go_day, datetime.time.max))
                                         ).order_by('price_adult')[:10]
        else:
            return Ticket.objects.all()[:10]

    @staticmethod
    def get_by_date(date):
        lst = Ticket.object.filter(departure_time__exact=date)
        return lst
