#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
# import datetime

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

    # reference

    # ref = models.IntegerField(default=0)


class VJATicket(models.Model):
    """List all ticket of VietJet"""
    # promo
    promo_num = models.IntegerField(default=20)
    pro_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pro_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pro_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pro_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pro_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pro_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # eco
    eco_num = models.IntegerField(default=20)
    eco_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    eco_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    eco_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    eco_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    eco_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    eco_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # skyboss
    skyboss_num = models.IntegerField(default=20)
    sky_adult_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sky_child_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sky_babe_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sky_adult_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sky_child_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    sky_babe_ft = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)

    # ref = models.IntegerField(default=0)


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

    # ref = models.IntegerField(default=0)


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
    ticket = models.IntegerField(default=0)
    # up_ref = models.BooleanField(default=True)
    carrier = models.CharField(max_length=5, default='vna')
    flight_code = models.CharField(max_length=10, default='VN370')
    date_created = models.DateTimeField(default=timezone.now)

    # carrier = vna, vja, pja
    # type = flex, standard, save, none
    # sit_class = FIRST, BUSINESS, ECONOMY, SAVE
    # def delete(self, using=None, keep_parents=False):
    #     q = VJATicket.objects.get(id=self.ticket)
    #     q.ref -= 1
    #     q.save()

    def save(self, *args, **kwargs):
        # if self.carrier == 'vja' and self.up_ref:
        #     q = VJATicket.objects.get(id=self.ticket)
        #     q.ref += 1
        #     self.up_ref = False
        #     q.save()
        # elif self.carrier == 'vna' and self.up_ref:
        #     q = VNATicket.objects.get(id=self.ticket)
        #     q.ref += 1
        #     self.up_ref = False
        #     q.save()
        # elif self.carrier == 'jsa' and self.up_ref:
        #     q = JSATicket.objects.get(id=self.ticket)
        #     q.ref += 1
        #     self.up_ref = False
        #     q.save()

        if not self.arrival_time:
            self.arrival_time = None
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + "_" + unicode(self.departure_port) + "_" + \
               unicode(self.arrival_port) +\
               "_" + unicode(self.departure_time.date().strftime("%y%m%d"))


##############################################################################################
#
#    WELCOME TO THE INTERNATIONAL --- * --- TRANSIT
#
##############################################################################################


class IntAirport(models.Model):
    """ International airport """
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=160)
    # short name for airport e.g. Ho Chi Minh (SGN)
    sname = models.CharField(max_length=80, default=None)
    # List airport connected
    router = models.CharField(max_length=100, default=None)
    is_del = models.BooleanField(default=False)
    # additional for transit

    # continent = ['ASIA', 'EURO', 'AFRI', 'NAMER', 'SAMER', 'AUS']
    continent = models.CharField(max_length=5, default='ASIA')
    # region hien tai se chi la sea thoi :)
    # now only have 'sea' region, bobo putang ina mo
    region = models.CharField(max_length=9, default='SEA')
    # not importance
    nation = models.CharField(max_length=55, default='Vatican')

    def __str__(self):
        return str(self.id) + '_' + unicode(self.code) + '_' + unicode(self.sname) + \
               '_' + unicode(self.nation) + '_' + unicode(self.region) + '_' + unicode(self.continent)


class IntContinentRoute(models.Model):
    departure_cont = models.CharField(max_length=10)
    arrival_cont = models.CharField(max_length=10)
    route_cont = models.CharField(max_length=150)
    date_create = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


class IntRegionRoute(models.Model):
    departure_region = models.CharField(max_length=10)
    arrival_region = models.CharField(max_length=10)
    route_region = models.CharField(max_length=160)
    date_create = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


class IntConnectingMap(models.Model):
    departure_port = models.CharField(max_length=10)
    arrival_port = models.CharField(max_length=10)
    have_direct = models.BooleanField(default=False)
    recommend = models.BooleanField(default=False)
    route_transit_once = models.CharField(max_length=160)
    route_transit_twice = models.CharField(max_length=160)
    date_create = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)


class IntTicket(models.Model):
    """ A set of price for a ticket in any type"""
    # carrier code
    carrier_code = models.CharField(max_length=25)

    carrier_name = models.CharField(max_length=225)

    ticket_type = models.CharField(max_length=225, default='normal')

    price_adult = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    price_child = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    price_babe = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    fee_tax_adult = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    fee_tax_child = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    fee_tax_babe = models.DecimalField(default=0.0, decimal_places=2, max_digits=15)
    is_del = models.BooleanField(default=False)


class IntFlight(models.Model):
    """ International flight """
    # departure_port = models.ForeignKey(
    #     Airport,
    #     to_field='code',
    #     db_column="departure_port",
    #     on_delete=models.CASCADE,
    #     related_name='dep_code',
    #     related_query_name='depart'
    # )
    # arrival_port = models.ForeignKey(
    #     Airport,
    #     to_field='code',
    #     db_column='arrival_port',
    #     on_delete=models.CASCADE,
    #     related_name='arr_code',
    #     related_query_name='arrival'
    # )

    departure_port = models.CharField(max_length=10)
    arrival_port = models.CharField(max_length=10)
    departure_time = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    ticket = models.CharField(max_length=160)
    # e.g. 12,13,42,... a list number, which is id of ticket in IntTicket Table
    # up_ref = models.BooleanField(default=True)
    carrier = models.CharField(max_length=7, default='vna')
    flight_code = models.CharField(max_length=10, default='VN370')
    date_created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + "_" + unicode(self.departure_port) + "_" + \
               unicode(self.arrival_port) + \
               "_" + unicode(self.departure_time.date().strftime("%y%m%d"))
