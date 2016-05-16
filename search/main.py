#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import Ticket, Carrier, Airport
from django.db.models import F
from .models import timezone
import random
import datetime


class Main (object):
    """Lõi xử lý chính"""

    @staticmethod
    def get_by_date(date):
        lst = Ticket.object.filter(departure_time__exact=date)
        return lst

    @staticmethod
    def make_some_db():
        day = 22
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
                in1 = 21-in2
            td1 = td(hours=rr(0, 23), minutes=5*rr(0, 11))
            td2 = td1 + td(hours=rr(0, 23), minutes=5*rr(0, 11))
            t = Ticket(departure_port=ap(pk=in1) ,
                       arrival_port_id=ap(pk=in2),
                       departure_time=date + td1,
                       arrival_time=date + td2,
                       price=100*rr(2, 21),
                       ticket_type=rc(ticket_type),
                       sit_class=rc(sit_class),
                       carrier=rc(carry),
                       date_created=timezone.now()
                       )
            t.save()
