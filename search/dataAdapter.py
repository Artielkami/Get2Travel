#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import Ticket, Airport, Carrier, DomesticRegion, MiddlePort
import datetime
import random
from django.utils import timezone


class DataAdapter(object):

    """Class chứa các hàm xử lí tạo dữ liẹu giả, hoặc đưa dữ liệu thật vào database,
     kết xuất dữ liệu, và một số tác vụ khác"""

    @staticmethod
    def make_routes():
        airport = Airport.objects.values_list('code', flat=True)
        maping = {}
        j = ','.join
        for ap in Airport.objects.all():
            maping[ap.code] = ap.router.split(',')
        for dep in airport:
            for arr in airport:
                tmp = maping[dep]

                routes = []
                for item in tmp:
                    if arr in maping[item]:
                        routes.append(item)
                mp = MiddlePort(depart_port=dep,
                                arrival_port=arr,
                                middle_port=j(routes))
                mp.save()

    @staticmethod
    def del_all_routes():
        MiddlePort.objects.all().delete()

    @staticmethod
    def make_some_db():
        day = 23
        date = datetime.datetime(year=2016, month=5, day=day,
                                 hour=0, minute=0, second=0)
        td = datetime.timedelta
        ticket_type = ['ADU', 'CHI', 'SEN']
        carry = ['Ppew', 'UFO', 'Aiur', 'Navi', 'Medin', 'Lotha', 'Sinvo',
                 'Valve', 'Volvo', 'Skys']
        sit_class = ['BUSINESS', 'NORMAL', 'FIRST']
        ap = Airport.objects.get
        rc = random.choice
        rr = random.randrange
        for x in xrange(1, 100):
            print 'make', x
            in1 = rr(1, 21)
            in2 = rr(1, 21)
            if in1 == in2:
                in1 = 21 - in2
            td1 = td(hours=rr(0, 23), minutes=5 * rr(0, 11))
            td2 = td1 + td(hours=rr(0, 23), minutes=5 * rr(0, 11))
            t = Ticket(departure_port=ap(pk=in1),
                       arrival_port_id=ap(pk=in2),
                       departure_time=date + td1,
                       arrival_time=date + td2,
                       price=100 * rr(2, 21),
                       ticket_type=rc(ticket_type),
                       sit_class=rc(sit_class),
                       carrier=rc(carry),
                       date_created=timezone.now()
                       )
            t.save()
