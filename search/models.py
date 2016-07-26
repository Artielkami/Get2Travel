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
    sname = models.CharField(max_length=50, default=None)
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
    is_del = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + '_' + unicode(self.code) + '_' + unicode(self.name)


class DomesticRegion(models.Model):
    name = models.CharField(max_length=25)
    airport = models.CharField(max_length=5)
    value = models.IntegerField(default=0)


class MiddlePort(models.Model):
    depart_port = models.CharField(max_length=5)
    arrival_port = models.CharField(max_length=5)
    middle_port = models.CharField(max_length=100)
    is_del = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + '_' + unicode(self.depart_port) + '_' + unicode(self.arrival_port)


class VNATicket(models.Model):
    """List all ticket of VN Airlines"""
    # business flex
    business_flex_num = models.IntegerField(default=20)
    bf_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    bf_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    bf_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    bf_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    bf_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    bf_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # business standard
    business_standard_num = models.IntegerField(default=20)
    bs_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    bs_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    bs_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    bs_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    bs_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    bs_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # economy flex
    economy_flex_num = models.IntegerField(default=20)
    ef_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    ef_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    ef_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    ef_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    ef_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    ef_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # economy standard
    economy_standard_num = models.IntegerField(default=20)
    es_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    es_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    es_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    es_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    es_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    es_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # economy save
    economy_save_num = models.IntegerField(default=20)
    esa_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    esa_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    esa_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    esa_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    esa_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    esa_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # special deal
    special_deal_num = models.IntegerField(default=20)
    sd_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sd_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sd_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sd_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sd_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sd_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)


class VJATicket(models.Model):
    """List all ticket of VietJet"""
    # business flex
    promo_num = models.IntegerField(default=20)
    pro_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pro_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pro_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pro_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pro_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pro_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # business standard
    eco_num = models.IntegerField(default=20)
    eco_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    eco_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    eco_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    eco_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    eco_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    eco_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # economy flex
    skyboss_num = models.IntegerField(default=20)
    sky_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sky_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sky_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sky_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sky_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sky_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)


class JSATicket(models.Model):
    """List all ticket of JetStar"""
    # business flex
    save_num = models.IntegerField(default=20)
    save_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    save_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    save_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    save_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    save_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    save_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # business standard
    flex_num = models.IntegerField(default=20)
    flex_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    flex_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    flex_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    flex_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    flex_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    flex_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # economy flex
    optimize_num = models.IntegerField(default=20)
    opt_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    opt_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    opt_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    opt_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    opt_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    opt_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)


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
    # price_adult = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    # price_child = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    # price_babe = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    # fee_tax_adult = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    # fee_tax_child = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    # fee_tax_babe = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    # ticket_type = models.CharField(max_length=50, null=False, default=None)
    # sit_class = models.CharField(max_length=20, default='business')
    ticket = models.IntegerField()
    carrier = models.CharField(max_length=5, default='vna')
    flight_code = models.CharField(max_length=10, default='VN370')
    date_created = models.DateTimeField(default=timezone.now)

    # carrier = vna, vja, pja
    # type = flex, standard, save, none
    # sit_class = FIRST, BUSINESS, ECONOMY, SAVE

    def save(self, *args, **kwargs):
        if not self.arrival_time:
            self.arrival_time = None
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + "_" + unicode(self.departure_port) + "_" + \
               unicode(self.arrival_port) +\
               "_" + unicode(self.departure_time.date().strftime("%y%m%d"))
