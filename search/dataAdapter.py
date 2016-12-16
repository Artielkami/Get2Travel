#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import Ticket, Airport, Carrier, DomesticRegion, \
    MiddlePort, VNATicket, VJATicket, JSATicket, \
    IntFlight, IntTicket, IntAirport, IntConnectingMap,\
    IntContinentRoute, IntRegionRoute
import datetime
import random
from django.utils import timezone


class DataAdapter(object):

    """ Class chứa các hàm xử lí tạo dữ liẹu giả, hoặc đưa dữ liệu thật vào database,
     kết xuất dữ liệu, và một số tác vụ khác """

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
    def make_some_db_2():
        """Create fake data for test"""
        day = 22
        date = datetime.datetime(year=2016, month=12, day=day,
                                 hour=0, minute=0, second=0)
        td = datetime.timedelta
        #type = ['standard', 'save', 'flex']
        # type_bu = ['standard', 'flex']
        # carry = ['Ppew', 'UFO', 'Aiur', 'Navi', 'Medin', 'Lotha', 'Sinvo',
        #          'Valve', 'Volvo', 'Skys']
        carry = ['vna', 'vja', 'jsa']
        #sit_class = ['economy', 'business', 'first', 'save']
        fcode = ['VN370', 'VN7770', 'VJ1280', 'PJ8010', 'VJ780', 'PJ980']
        ap = IntAirport.objects.get
        rc = random.choice
        rr = random.randint
        for x in xrange(1, 20):
            print 'make', x
            # in1 = rr(1, 21)
            # in2 = rr(1, 21)
            # if in1 == in2:
            #     in1 = 21 - in2
            td1 = td(hours=rr(0, 23), minutes=5 * rr(0, 11))
            td2 = td1 + td(hours=rr(0, 23), minutes=5 * rr(0, 11))
            #sit = rc(sit_class)
            #typ = rc(type)
            # if sit == 'first' or sit == 'save':
            #     typ = None
            # elif sit == 'business' and typ == 'save':
            #     typ = 'standard'
            pr1 = rr(1, 3)
            pr2 = pr1 - 100*rr(3,5) if pr1 > 600 else pr1-100*rr(1,2)
            #pr3 = 0 if typ == 'save' else 100*rr(1,2)
            #ft1 = pr1*38/100
            #ft2 = pr2*29/100
            #ft3 = 100*rr(0, 1) + pr3*1/10

            t = IntFlight(departure_port='SGP',
                          arrival_port='HAN',  # ap(pk=in2),
                          departure_time=date + td1,
                          arrival_time=date + td2,
                          ticket=pr1,
                          # carrier=rc(carry),
                          carrier='vna',
                          flight_code=rc(fcode),
                          date_created=timezone.now()
                          )
            t.save()

    @staticmethod
    def make_sticket_domestic():
        rc = random.choice
        rr = random.randrange
        for index in range(1, 300):
            print '--- run ---'
            chance_pro = rr(1, 11)

            if chance_pro < 7:
                chance_pro = 0

            value_sky = rr(125, 350)*10
            value_eco = rr(60, 96)*10
            value_pro = rr(40, 80)*10*chance_pro

            factor_child = rr(35, 66)
            factor_infant = rr(0, 17)

            fee_n_tax = rr(14, 25)

            vja = VJATicket(promo_num=chance_pro,
                            pro_adult_price=value_pro,
                            pro_adult_ft=value_pro*fee_n_tax/100,
                            pro_babe_price=value_pro*factor_infant/100,
                            pro_babe_ft=value_pro*factor_infant*fee_n_tax/10000,
                            pro_child_price=value_pro*factor_child/100,
                            pro_child_ft=value_pro*factor_child*fee_n_tax/10000,
                            eco_num=10,
                            eco_adult_price=value_eco,
                            eco_adult_ft=value_eco * fee_n_tax/100,
                            eco_babe_price=value_eco * factor_infant/100,
                            eco_babe_ft=value_eco * factor_infant * fee_n_tax/10000,
                            eco_child_price=value_eco * factor_child/100,
                            eco_child_ft=value_eco * factor_child * fee_n_tax/10000,
                            skyboss_num=10,
                            sky_adult_price=value_sky,
                            sky_adult_ft=value_sky * fee_n_tax/100,
                            sky_babe_price=value_sky * factor_infant/100,
                            sky_babe_ft=value_sky * factor_infant * fee_n_tax/10000,
                            sky_child_price=value_sky * factor_child/100,
                            sky_child_ft=value_sky * factor_child * fee_n_tax/10000,
                            )
            vja.save()

            value_opt = rr(225, 380) * 10
            value_flex = rr(96, 166) * 10
            value_save = rr(65, 89) * 10

            jsa = JSATicket(save_num=10,
                            save_adult_price=value_save,
                            save_adult_ft=value_save * fee_n_tax / 100,
                            save_babe_price=value_save * factor_infant / 100,
                            save_babe_ft=value_save * factor_infant * fee_n_tax / 10000,
                            save_child_price=value_save * factor_child / 100,
                            save_child_ft=value_save * factor_child * fee_n_tax / 10000,
                            flex_num=10,
                            flex_adult_price=value_flex,
                            flex_adult_ft=value_flex * fee_n_tax / 100,
                            flex_babe_price=value_flex * factor_infant / 100,
                            flex_babe_ft=value_flex * factor_infant * fee_n_tax / 10000,
                            flex_child_price=value_flex * factor_child / 100,
                            flex_child_ft=value_flex * factor_child * fee_n_tax / 10000,
                            optimize_num=10,
                            opt_adult_price=value_opt,
                            opt_adult_ft=value_opt * fee_n_tax / 100,
                            opt_babe_price=value_opt * factor_infant / 100,
                            opt_babe_ft=value_opt * factor_infant * fee_n_tax / 10000,
                            opt_child_price=value_opt * factor_child / 100,
                            opt_child_ft=value_opt * factor_child * fee_n_tax / 10000,
                            )
            jsa.save()

            value_bf = rr(328, 520) * 10
            value_bs = rr(290, 322) * 10
            value_ef = rr(235, 289) * 10
            value_es = rr(183, 232) * 10
            value_esa = rr(120, 166) * 10
            value_sd = rr(66, 82) * chance_pro

            vna = VNATicket(
                            business_flex_num=10,
                            bf_adult_price=value_bf,
                            bf_adult_ft=value_bf * fee_n_tax / 100,
                            bf_babe_price=value_bf * factor_infant / 100,
                            bf_babe_ft=value_bf * factor_infant * fee_n_tax / 10000,
                            bf_child_price=value_bf * factor_child / 100,
                            bf_child_ft=value_bf * factor_child * fee_n_tax / 10000,
                            business_standard_num=10,
                            bs_adult_price=value_bs,
                            bs_adult_ft=value_bs * fee_n_tax / 100,
                            bs_babe_price=value_bs * factor_infant / 100,
                            bs_babe_ft=value_bs * factor_infant * fee_n_tax / 10000,
                            bs_child_price=value_bs * factor_child / 100,
                            bs_child_ft=value_bs * factor_child * fee_n_tax / 10000,
                            economy_flex_num=10,
                            ef_adult_price=value_ef,
                            ef_adult_ft=value_ef * fee_n_tax / 100,
                            ef_babe_price=value_ef * factor_infant / 100,
                            ef_babe_ft=value_ef * factor_infant * fee_n_tax / 10000,
                            ef_child_price=value_ef * factor_child / 100,
                            ef_child_ft=value_ef * factor_child * fee_n_tax / 10000,
                            special_deal_num=chance_pro,
                            sd_adult_price=value_sd,
                            sd_adult_ft=value_sd * fee_n_tax / 100,
                            sd_babe_price=value_sd * factor_infant / 100,
                            sd_babe_ft=value_sd * factor_infant * fee_n_tax / 10000,
                            sd_child_price=value_sd * factor_child / 100,
                            sd_child_ft=value_sd * factor_child * fee_n_tax / 10000,
                            economy_standard_num=10,
                            es_adult_price=value_es,
                            es_adult_ft=value_es * fee_n_tax / 100,
                            es_babe_price=value_es * factor_infant / 100,
                            es_babe_ft=value_es * factor_infant * fee_n_tax / 10000,
                            es_child_price=value_es * factor_child / 100,
                            es_child_ft=value_es * factor_child * fee_n_tax / 10000,
                            economy_save_num=10,
                            esa_adult_price=value_esa,
                            esa_adult_ft=value_esa * fee_n_tax / 100,
                            esa_babe_price=value_esa * factor_infant / 100,
                            esa_babe_ft=value_esa * factor_infant * fee_n_tax / 10000,
                            esa_child_price=value_esa * factor_child / 100,
                            esa_child_ft=value_esa * factor_child * fee_n_tax / 10000,
                            )
            vna.save()
            
            
    @staticmethod
    def make_some_db():
        """Create fake data for test"""
        day = 27
        date = datetime.datetime(year=2017, month=1, day=day,
                                 hour=0, minute=0, second=0)
        td = datetime.timedelta
        # type = ['standard', 'save', 'flex']
        # type_bu = ['standard', 'flex']
        # carry = ['Ppew', 'UFO', 'Aiur', 'Navi', 'Medin', 'Lotha', 'Sinvo',
        #          'Valve', 'Volvo', 'Skys']
        carry = ['vna', 'vja', 'jsa']
        # sit_class = ['economy', 'business', 'first', 'save']

        ap = Airport.objects.get
        rc = random.choice
        rr = random.randrange
        for x in xrange(1, 500):
            print 'make_tk', x
            in1 = rr(1, 21)
            in2 = rr(1, 21)
            while in2 == in1:
                in2 = rr(1, 21)
            td1 = td(hours=rr(0, 23), minutes=5 * rr(0, 11))
            td2 = td1 + td(hours=rr(0, 23), minutes=5 * rr(0, 11))
            # sit = rc(sit_class)
            # typ = rc(type)
            # if sit == 'first' or sit == 'save':
            #     typ = None
            # elif sit == 'business' and typ == 'save':
            #     typ = 'standard'
            pr1 = rr(1, 300)
            # pr2 = pr1 - 100 * rr(3, 5) if pr1 > 600 else pr1 - 100 * rr(1, 2)
            # pr3 = 0 if typ == 'save' else 100*rr(1,2)
            # ft1 = pr1*38/100
            # ft2 = pr2*29/100
            # ft3 = 100*rr(0, 1) + pr3*1/10

            carrier = rc(carry)
            f_code_num = rr(12, 89)*10
            if carrier == 'vja':
                f_code = 'VJ' + str(f_code_num)
            if carrier == 'jsa':
                f_code = 'JS' + str(f_code_num)
            if carrier == 'vna':
                f_code = 'VN' + str(f_code_num)

            t = Ticket(departure_port=ap(pk=in1),
                       arrival_port=ap(pk=in2),
                       departure_time=date + td1,
                       arrival_time=date + td2,
                       ticket=pr1,
                       carrier=carrier,
                       flight_code=f_code,
                       date_created=timezone.now()
                       )
            t.save()