#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import Ticket, Carrier, Airport, MiddlePort, VNATicket, VJATicket, JSATicket
from django.db.models import F
from result import Result, Flight
import random
import datetime


class SeatFlight(object):
    def __init__(self):
        self.ticket_type = 0
        self.adult_price = 0
        self.child_price = 0
        self.babe_price = 0
        self.adult_ft = 0
        self.child_ft = 0
        self.babe_ft = 0


class AFlight(object):
    def __init__(self):
        self.total_price_min = 0
        self.departure_port = None
        self.arrival_port = None
        self.departure_time = '0000'
        self.arrival_time = '0000'
        self.seat_list = []


class ResultFlight(object):
    def __init__(self):
        self.total_price = 0
        self.transit = None
        self.departure_time = '0000'
        self.arrival_time = '0000'
        self.first_flight = []
        self.second_flight = []


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

    def search(self, data = {}):
        self.num_adult = data['adult']
        self.num_child = data['child']
        self.num_infan = data['babe']
        self.outward_day = data['go_day']
        self.return_day = data['rt_day']
        self.way = data['way']
        self.dep_port = data['departure']
        self.arr_port = data['arrival']
        transit_list = MiddlePort.objects.filter(depart_port=self.dep_port, arrival_port=self.arr_port)
        flight_lst = Ticket.objects.filter(departure_port=self.dep_port,
                                           arrival_port=self.arr_port,
                                           departure_time__range=(
                                               datetime.datetime.combine(self.outward_day, datetime.time.min),
                                               datetime.datetime.combine(self.outward_day, datetime.time.max))
                                           )
        # TODO --------- search method ---------
        if flight_lst:
            for flight in flight_lst:
                # get list ticket suitable with carrier
                if flight.carrier == 'vna':
                    ticket_lst = VNATicket.objects.get(id=flight.ticket)
                elif flight.carrier == 'vja':
                    ticket_lst = VJATicket.objects.get(id=flight.ticket)
                elif flight.carrier == 'jsa':
                    ticket_lst = JSATicket.objects.get(id=flight.ticket)
                aResult = ResultFlight()

    @staticmethod
    def get_ticket(dep, arr, go_day, rt_day='xxx', way=1, stop=0, ttype='all', quan = {}):
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
