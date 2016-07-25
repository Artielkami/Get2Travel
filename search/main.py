#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import Ticket, Carrier, Airport, MiddlePort
from django.db.models import F
from result import Result, Flight
import random
import datetime

class Main(object):
    """Lõi xử lý chính"""
    def __init__(self):
        self.num_adult = 0
        self.num_child = 0
        self.num_infan = 0
        self.outward_day = None
        self.return_day = None
        self.way = 1  # chieu di, la 1/2 chieu
        self.dep_port = None
        self.arr_port = None
        self.sort_by = 'price'
        self.outward_list = []
        self.return_list = []

    @staticmethod
    def get_ticket(dep, arr, go_day, rt_day='xxx', way=1, stop=0, ttype='all'):
        if ttype == 'all' and (stop == 0 or stop == 1):
            return Ticket.objects.filter(departure_port=dep,
                                         arrival_port=arr,
                                         departure_time__range=(datetime.datetime.combine(go_day, datetime.time.min),
                                                                datetime.datetime.combine(go_day, datetime.time.max))
                                         ).order_by('price_adult')[:10]
        elif stop == 2:
            routes_str = MiddlePort.objects.get(depart_port=dep,
                                                arrival_port=arr)
            if routes_str:
                routes_lst = routes_str.middle_port.split(',')
                print routes_lst[0]
                # for routes in routes_lst:
                if ttype == 'all':
                    flight_lst = Ticket.objects.filter(departure_port=dep,
                                                       arrival_port=routes_lst[0],
                                                       departure_time__range=(
                                                       datetime.datetime.combine(go_day, datetime.time.min),
                                                       datetime.datetime.combine(go_day, datetime.time.max))
                                                       ).order_by('price_adult')[:5]

                else:
                    flight_lst = Ticket.objects.filter(departure_port=dep,
                                                       arrival_port=routes_lst[0],
                                                       sit_class=ttype,
                                                       departure_time__range=(
                                                       datetime.datetime.combine(go_day, datetime.time.min),
                                                       datetime.datetime.combine(go_day, datetime.time.max))
                                                       ).order_by('price_adult')[:5]
                td = datetime.timedelta
                rs_routes_search = []
                for item in flight_lst:
                    print item.id
                for flight in flight_lst:
                    tmp = Ticket.objects.filter(departure_port=routes_lst[0],
                                                arrival_port=arr,
                                                departure_time__range=(
                                                    flight.arrival_time + td(hours=1, minutes=20),
                                                    flight.arrival_time + td(hours=6, minutes=10)
                                                )
                                                ).order_by('price_adult')[:3]
                    if tmp:
                        rs_routes_search.append((flight, tmp))
                return rs_routes_search
            else:
                return None
        else:
            return Ticket.objects.filter(departure_port=dep,
                                         arrival_port=arr,
                                         sit_class=ttype,
                                         departure_time__range=(datetime.datetime.combine(go_day, datetime.time.min),
                                                                datetime.datetime.combine(go_day, datetime.time.max))
                                         ).order_by('price_adult')[:10]

    @staticmethod
    def get_by_date(date):
        lst = Ticket.object.filter(departure_time__exact=date)
        return lst
