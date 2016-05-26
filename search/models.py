#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
import datetime

# Create your models here.


class Airport(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=60)
    router = models.CharField(max_length=100, default='xxx')
    is_del = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + '_' + unicode(self.code) + '_' + unicode(self.name)

    def __unicode__(self):
        return u'%s' % self.code


class Carrier(models.Model):
    code = models.CharField(max_length=9)
    name = models.CharField(max_length=70)
    type = models.CharField(max_length=9)


class DomesticRegion(models.Model):
    name = models.CharField(max_length=25)
    airport = models.CharField(max_length=5)
    value = models.IntegerField(default=0)


class MiddlePort(models.Model):
    depart_port = models.CharField(max_length=5)
    arrival_port = models.CharField(max_length=5)
    middle_port = models.CharField(max_length=100)
    is_del = models.BooleanField(default=False)


class Ticket(models.Model):
    departure_port = models.ForeignKey(
        Airport,
        to_field='code',
        db_column="departure_port",
        on_delete=models.CASCADE,
        related_name='dep_code',
        related_query_name='depart'
    )
    arrival_port = models.ForeignKey(
        Airport,
        to_field='code',
        db_column='arrival_port',
        on_delete=models.CASCADE,
        related_name='arr_code',
        related_query_name='arrival'
    )
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    ticket_type = models.CharField(max_length=25, default='Normal')
    sit_class = models.CharField(max_length=20, default='Trevaler')
    carrier = models.CharField(max_length=5, default='Aiur')
    date_created = models.DateTimeField(default=timezone.now)

    # type = ADU, CHI, SEN
    # sit_type = FIRST, BUSINESS, NORMAL

    def save(self, *args, **kwargs):
        if not self.arrival_time:
            self.arrival_time = None
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + "_" + unicode(self.departure_port) + "_" + \
               unicode(self.arrival_port) +\
               "_" + unicode(self.departure_time.date().strftime("%y%m%d"))