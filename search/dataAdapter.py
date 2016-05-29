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
    def del_all_ticket():
        Ticket.objects.all().delete()

    @staticmethod
    def make_some_db():
        day = 20
        date = datetime.datetime(year=2016, month=5, day=day,
                                 hour=0, minute=0, second=0)
        td = datetime.timedelta
        type = ['standard', 'save', 'flex']
        # type_bu = ['standard', 'flex']
        # carry = ['Ppew', 'UFO', 'Aiur', 'Navi', 'Medin', 'Lotha', 'Sinvo',
        #          'Valve', 'Volvo', 'Skys']
        carry = ['vna', 'vja', 'pja']
        sit_class = ['economy', 'business', 'first', 'save']
        fcode = ['VN370', 'VN7770', 'VJ1280', 'PJ8010', 'VJ780', 'PJ980']
        ap = Airport.objects.get
        rc = random.choice
        rr = random.randrange
        for x in xrange(1, 200):
            print 'make', x
            in1 = rr(1, 21)
            in2 = rr(1, 21)
            if in1 == in2:
                in1 = 21 - in2
            td1 = td(hours=rr(0, 23), minutes=5 * rr(0, 11))
            td2 = td1 + td(hours=rr(0, 23), minutes=5 * rr(0, 11))
            sit = rc(sit_class)
            typ = rc(type)
            if sit == 'first' or sit == 'save':
                typ = None
            elif sit == 'business' and typ == 'save':
                typ = 'standard'
            pr1 = 100 * rr(4, 21)
            pr2 = pr1 - 100*rr(3,5) if pr1 > 600 else pr1-100*rr(1,2)
            pr3 = 0 if typ == 'save' else 100*rr(1,2)
            ft1 = pr1*38/100
            ft2 = pr2*29/100
            ft3 = 100*rr(0,1) + pr3*1/10
            t = Ticket(departure_port=ap(pk=in1),
                       arrival_port=ap(pk=in2),
                       departure_time=date + td1,
                       arrival_time=date + td2,
                       price_adult =pr1,
                       price_child=pr2,
                       price_babe=pr3,
                       fee_tax_adult=ft1,
                       fee_tax_child=ft2,
                       fee_tax_babe=ft3,
                       ticket_type=typ,
                       sit_class=sit,
                       carrier=rc(carry),
                       flight_code=rc(fcode),
                       date_created=timezone.now()
                       )
            t.save()
