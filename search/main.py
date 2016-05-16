#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import Ticket, Carrier
from django.db.models import F

class Main (object):
    """Lõi xử lý chính"""

    def get_by_date(date):
        lst = Ticket.object.filter(departure_time__exact=date)
        return lst
