#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import Ticket, Carrier, Airport, MiddlePort, VNATicket, VJATicket, JSATicket
from django.db.models import F
from result import Result, Flight
import random
import datetime


class SeatFlight(object):
    def __init__(self, ticket_type=None, adult_price=0, child_price=0,
                 babe_price=0, adult_ft=0, child_ft=0, babe_ft=0):
        self.ticket_type = ticket_type
        self.total_price = 0
        self.total_ticket_price = 0
        self.total_ticket_fee = 0
        self.adult_price = adult_price
        self.child_price = child_price
        self.babe_price = babe_price
        self.adult_ft = adult_ft
        self.child_ft = child_ft
        self.babe_ft = babe_ft

    def set_price(self, num_adult=0, num_child=0, num_babe=0):
        self.total_ticket_price = num_adult * self.adult_price + \
                                  num_child * self.child_price + \
                                  num_babe * self.babe_price
        self.total_ticket_fee = num_adult * self.adult_ft + \
                                num_child * self.child_ft + \
                                num_babe * self.babe_ft
        self.total_price += self.total_price + self.total_ticket_fee


class AFlight(object):
    def __init__(self):
        self.total_price_min = 0
        self.carrier = None
        self.flight_code = None
        self.departure_port = None
        self.arrival_port = None
        self.departure_name = None
        self.arrival_name = None
        self.departure_time = '0000'
        self.arrival_time = '0000'
        self.seat_list = []

    def set_min_price(self):
        for seat in self.seat_list:
            if self.total_price_min == 0 or self.total_price_min < seat.total_price:
                self.total_price_min = seat.total_price


class ResultFlight(object):
    def __init__(self, transit=None):
        self.total_price = 0
        self.transit = transit
        self.departure_time = '0000'
        self.arrival_time = '0000'
        self.end_port = None
        self.first_flight = None
        self.second_flight = []

    def set_price(self):
        self.total_price = self.first_flight.total_price_min
        if self.transit:
            second_min_price = 0
            for flight in self.second_flight:
                if second_min_price == 0 or flight.total_price_min < second_min_price:
                    second_min_price = flight.total_price_min
            self.total_price += second_min_price


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

    # search method
    # the most importance action
    def search(self, data={}):
        self.num_adult = data['adult']
        self.num_child = data['child']
        self.num_infan = data['babe']
        self.outward_day = data['go_day']
        self.return_day = data['rt_day']
        self.way = data['way']
        self.dep_port = data['departure']
        self.arr_port = data['arrival']
        td = datetime.timedelta
        num_passenger = self.num_adult + self.num_child + self.num_infan
        transit_list = MiddlePort.objects.get(depart_port=self.dep_port, arrival_port=self.arr_port)

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
                lst_ticket = []
                if flight.carrier == 'vna':
                    ticket_lst = VNATicket.objects.get(id=flight.ticket)
                    # business flex
                    ticket_vnabf = SeatFlight(ticket_type='vna_bf',
                                              adult_price=ticket_lst.bf_adult_price,
                                              child_price=ticket_lst.bf_child_price,
                                              babe_price=ticket_lst.bf_babe_price,
                                              adult_ft=ticket_lst.bf_adult_ft,
                                              child_ft=ticket_lst.bf_child_ft,
                                              babe_ft=ticket_lst.bf_babe_ft)
                    ticket_vnabf.set_price(num_adult=self.num_adult,
                                           num_child=self.num_child,
                                           num_babe=self.num_infan)
                    # business standard
                    ticket_vnabs = SeatFlight(ticket_type='vna_bs',
                                              adult_price=ticket_lst.bs_adult_price,
                                              child_price=ticket_lst.bs_child_price,
                                              babe_price=ticket_lst.bs_babe_price,
                                              adult_ft=ticket_lst.bs_adult_ft,
                                              child_ft=ticket_lst.bs_child_ft,
                                              babe_ft=ticket_lst.bs_babe_ft)
                    ticket_vnabs.set_price(num_adult=self.num_adult,
                                           num_child=self.num_child,
                                           num_babe=self.num_infan)
                    # economy flex
                    ticket_vnaef = SeatFlight(ticket_type='vna_ef',
                                              adult_price=ticket_lst.ef_adult_price,
                                              child_price=ticket_lst.ef_child_price,
                                              babe_price=ticket_lst.ef_babe_price,
                                              adult_ft=ticket_lst.ef_adult_ft,
                                              child_ft=ticket_lst.ef_child_ft,
                                              babe_ft=ticket_lst.ef_babe_ft)
                    ticket_vnaef.set_price(num_adult=self.num_adult,
                                           num_child=self.num_child,
                                           num_babe=self.num_infan)
                    # economy standard
                    ticket_vnaes = SeatFlight(ticket_type='vna_es',
                                              adult_price=ticket_lst.es_adult_price,
                                              child_price=ticket_lst.es_child_price,
                                              babe_price=ticket_lst.es_babe_price,
                                              adult_ft=ticket_lst.es_adult_ft,
                                              child_ft=ticket_lst.es_child_ft,
                                              babe_ft=ticket_lst.es_babe_ft)
                    ticket_vnaes.set_price(num_adult=self.num_adult,
                                           num_child=self.num_child,
                                           num_babe=self.num_infan)
                    # economy save
                    ticket_vnaesa = SeatFlight(ticket_type='vna_esa',
                                               adult_price=ticket_lst.esa_adult_price,
                                               child_price=ticket_lst.esa_child_price,
                                               babe_price=ticket_lst.esa_babe_price,
                                               adult_ft=ticket_lst.esa_adult_ft,
                                               child_ft=ticket_lst.esa_child_ft,
                                               babe_ft=ticket_lst.esa_babe_ft)
                    ticket_vnaesa.set_price(num_adult=self.num_adult,
                                            num_child=self.num_child,
                                            num_babe=self.num_infan)
                    # special deal
                    ticket_vnasd = SeatFlight(ticket_type='vna_sd',
                                              adult_price=ticket_lst.sd_adult_price,
                                              child_price=ticket_lst.sd_child_price,
                                              babe_price=ticket_lst.sd_babe_price,
                                              adult_ft=ticket_lst.sd_adult_ft,
                                              child_ft=ticket_lst.sd_child_ft,
                                              babe_ft=ticket_lst.sd_babe_ft)
                    ticket_vnasd.set_price(num_adult=self.num_adult,
                                           num_child=self.num_child,
                                           num_babe=self.num_infan)

                    lst_ticket.append(ticket_vnabf)
                    lst_ticket.append(ticket_vnabs)
                    lst_ticket.append(ticket_vnaef)
                    lst_ticket.append(ticket_vnaes)
                    lst_ticket.append(ticket_vnaesa)
                    lst_ticket.append(ticket_vnasd)
                elif flight.carrier == 'vja':  # vietjetair
                    ticket_lst = VJATicket.objects.get(id=flight.ticket)
                    # promo
                    ticket_vjapromo = SeatFlight(ticket_type='vja_promo',
                                                 adult_price=ticket_lst.pro_adult_price,
                                                 child_price=ticket_lst.pro_child_price,
                                                 babe_price=ticket_lst.pro_babe_price,
                                                 adult_ft=ticket_lst.pro_adult_ft,
                                                 child_ft=ticket_lst.pro_child_ft,
                                                 babe_ft=ticket_lst.pro_babe_ft)
                    ticket_vjapromo.set_price(num_adult=self.num_adult,
                                              num_child=self.num_child,
                                              num_babe=self.num_infan)
                    # eco
                    ticket_vjaeco = SeatFlight(ticket_type='vja_eco',
                                               adult_price=ticket_lst.eco_adult_price,
                                               child_price=ticket_lst.eco_child_price,
                                               babe_price=ticket_lst.eco_babe_price,
                                               adult_ft=ticket_lst.eco_adult_ft,
                                               child_ft=ticket_lst.eco_child_ft,
                                               babe_ft=ticket_lst.eco_babe_ft)
                    ticket_vjaeco.set_price(num_adult=self.num_adult,
                                            num_child=self.num_child,
                                            num_babe=self.num_infan)
                    # skyboss
                    ticket_vjasky = SeatFlight(ticket_type='vja_sky',
                                               adult_price=ticket_lst.sky_adult_price,
                                               child_price=ticket_lst.sky_child_price,
                                               babe_price=ticket_lst.sky_babe_price,
                                               adult_ft=ticket_lst.sky_adult_ft,
                                               child_ft=ticket_lst.sky_child_ft,
                                               babe_ft=ticket_lst.sky_babe_ft)
                    ticket_vjasky.set_price(num_adult=self.num_adult,
                                            num_child=self.num_child,
                                            num_babe=self.num_infan)
                    lst_ticket.append(ticket_vjapromo)
                    lst_ticket.append(ticket_vjaeco)
                    lst_ticket.append(ticket_vjasky)
                elif flight.carrier == 'jsa':  # jetstar
                    ticket_lst = JSATicket.objects.get(id=flight.ticket)
                    # save
                    ticket_jsasave = SeatFlight(ticket_type='jsa_save',
                                                adult_price=ticket_lst.save_adult_price,
                                                child_price=ticket_lst.save_child_price,
                                                babe_price=ticket_lst.save_babe_price,
                                                adult_ft=ticket_lst.save_adult_ft,
                                                child_ft=ticket_lst.save_child_ft,
                                                babe_ft=ticket_lst.save_babe_ft)
                    ticket_jsasave.set_price(num_adult=self.num_adult,
                                             num_child=self.num_child,
                                             num_babe=self.num_infan)
                    # promo
                    ticket_jsaflex = SeatFlight(ticket_type='jsa_flex',
                                                adult_price=ticket_lst.flex_adult_price,
                                                child_price=ticket_lst.flex_child_price,
                                                babe_price=ticket_lst.flex_babe_price,
                                                adult_ft=ticket_lst.flex_adult_ft,
                                                child_ft=ticket_lst.flex_child_ft,
                                                babe_ft=ticket_lst.flex_babe_ft)
                    ticket_jsaflex.set_price(num_adult=self.num_adult,
                                             num_child=self.num_child,
                                             num_babe=self.num_infan)
                    # opt
                    ticket_jsaopt = SeatFlight(ticket_type='jsa_opt',
                                               adult_price=ticket_lst.opt_adult_price,
                                               child_price=ticket_lst.opt_child_price,
                                               babe_price=ticket_lst.opt_babe_price,
                                               adult_ft=ticket_lst.opt_adult_ft,
                                               child_ft=ticket_lst.opt_child_ft,
                                               babe_ft=ticket_lst.opt_babe_ft)
                    ticket_jsaopt.set_price(num_adult=self.num_adult,
                                            num_child=self.num_child,
                                            num_babe=self.num_infan)
                    lst_ticket.append(ticket_jsasave)
                    lst_ticket.append(ticket_jsaflex)
                    lst_ticket.append(ticket_jsaopt)
                aresult = ResultFlight()
                aflight = AFlight()

                # for seat in ticket_lst:
                aflight.seat_list = lst_ticket
                aflight.departure_port = flight.departure_port
                aflight.arrival_port = flight.arrival_port
                aflight.arrival_name = flight.arrival_port.sname
                aflight.departure_name = flight.departure_port.sname
                aflight.departure_time = flight.departure_time
                aflight.arrival_time = flight.arrival_time
                aflight.carrier = flight.carrier
                aflight.flight_code = flight.flight_code
                aflight.set_min_price()

                aresult.first_flight = aflight
                aresult.departure_time = flight.departure_time
                aresult.arrival_time = flight.arrival_time
                aresult.set_price()

                # Thêm kết quả tìm được vào list kết quả
                self.outward_list.append(aresult)
        if transit_list:
            lst_transit_port = transit_list.middle_port.split(',')
            for transit in lst_transit_port:
                first_flight_lst = Ticket.objects.filter(departure_port=self.dep_port,
                                                         arrival_port=transit,
                                                         departure_time__range=(
                                                             datetime.datetime.combine(self.outward_day,
                                                                                       datetime.time.min),
                                                             datetime.datetime.combine(self.outward_day,
                                                                                       datetime.time.max))
                                                         )
                if first_flight_lst:
                    for flight in first_flight_lst:
                        second_flight_lst = Ticket.objects.filter(departure_port=transit,
                                                                  arrival_port=self.arr_port,
                                                                  departure_time__range=(
                                                                      flight.arrival_time + td(hours=0, minutes=45),
                                                                      flight.arrival_time + td(hours=5, minutes=15)
                                                                  )
                                                                  )
                        if second_flight_lst:
                            lst_ticket = []
                            if flight.carrier == 'vna':
                                ticket_lst = VNATicket.objects.get(id=flight.ticket)
                                # business flex
                                ticket_vnabf = SeatFlight(ticket_type='vna_bf',
                                                          adult_price=ticket_lst.bf_adult_price,
                                                          child_price=ticket_lst.bf_child_price,
                                                          babe_price=ticket_lst.bf_babe_price,
                                                          adult_ft=ticket_lst.bf_adult_ft,
                                                          child_ft=ticket_lst.bf_child_ft,
                                                          babe_ft=ticket_lst.bf_babe_ft)
                                ticket_vnabf.set_price(num_adult=self.num_adult,
                                                       num_child=self.num_child,
                                                       num_babe=self.num_infan)
                                # business standard
                                ticket_vnabs = SeatFlight(ticket_type='vna_bs',
                                                          adult_price=ticket_lst.bs_adult_price,
                                                          child_price=ticket_lst.bs_child_price,
                                                          babe_price=ticket_lst.bs_babe_price,
                                                          adult_ft=ticket_lst.bs_adult_ft,
                                                          child_ft=ticket_lst.bs_child_ft,
                                                          babe_ft=ticket_lst.bs_babe_ft)
                                ticket_vnabs.set_price(num_adult=self.num_adult,
                                                       num_child=self.num_child,
                                                       num_babe=self.num_infan)
                                # economy flex
                                ticket_vnaef = SeatFlight(ticket_type='vna_ef',
                                                          adult_price=ticket_lst.ef_adult_price,
                                                          child_price=ticket_lst.ef_child_price,
                                                          babe_price=ticket_lst.ef_babe_price,
                                                          adult_ft=ticket_lst.ef_adult_ft,
                                                          child_ft=ticket_lst.ef_child_ft,
                                                          babe_ft=ticket_lst.ef_babe_ft)
                                ticket_vnaef.set_price(num_adult=self.num_adult,
                                                       num_child=self.num_child,
                                                       num_babe=self.num_infan)
                                # economy standard
                                ticket_vnaes = SeatFlight(ticket_type='vna_es',
                                                          adult_price=ticket_lst.es_adult_price,
                                                          child_price=ticket_lst.es_child_price,
                                                          babe_price=ticket_lst.es_babe_price,
                                                          adult_ft=ticket_lst.es_adult_ft,
                                                          child_ft=ticket_lst.es_child_ft,
                                                          babe_ft=ticket_lst.es_babe_ft)
                                ticket_vnaes.set_price(num_adult=self.num_adult,
                                                       num_child=self.num_child,
                                                       num_babe=self.num_infan)
                                # economy save
                                ticket_vnaesa = SeatFlight(ticket_type='vna_esa',
                                                           adult_price=ticket_lst.esa_adult_price,
                                                           child_price=ticket_lst.esa_child_price,
                                                           babe_price=ticket_lst.esa_babe_price,
                                                           adult_ft=ticket_lst.esa_adult_ft,
                                                           child_ft=ticket_lst.esa_child_ft,
                                                           babe_ft=ticket_lst.esa_babe_ft)
                                ticket_vnaesa.set_price(num_adult=self.num_adult,
                                                        num_child=self.num_child,
                                                        num_babe=self.num_infan)
                                # special deal
                                ticket_vnasd = SeatFlight(ticket_type='vna_sd',
                                                          adult_price=ticket_lst.sd_adult_price,
                                                          child_price=ticket_lst.sd_child_price,
                                                          babe_price=ticket_lst.sd_babe_price,
                                                          adult_ft=ticket_lst.sd_adult_ft,
                                                          child_ft=ticket_lst.sd_child_ft,
                                                          babe_ft=ticket_lst.sd_babe_ft)
                                ticket_vnasd.set_price(num_adult=self.num_adult,
                                                       num_child=self.num_child,
                                                       num_babe=self.num_infan)

                                lst_ticket.append(ticket_vnabf)
                                lst_ticket.append(ticket_vnabs)
                                lst_ticket.append(ticket_vnaef)
                                lst_ticket.append(ticket_vnaes)
                                lst_ticket.append(ticket_vnaesa)
                                lst_ticket.append(ticket_vnasd)
                            elif flight.carrier == 'vja':  # vietjetair
                                ticket_lst = VJATicket.objects.get(id=flight.ticket)
                                # promo
                                ticket_vjapromo = SeatFlight(ticket_type='vja_promo',
                                                             adult_price=ticket_lst.pro_adult_price,
                                                             child_price=ticket_lst.pro_child_price,
                                                             babe_price=ticket_lst.pro_babe_price,
                                                             adult_ft=ticket_lst.pro_adult_ft,
                                                             child_ft=ticket_lst.pro_child_ft,
                                                             babe_ft=ticket_lst.pro_babe_ft)
                                ticket_vjapromo.set_price(num_adult=self.num_adult,
                                                          num_child=self.num_child,
                                                          num_babe=self.num_infan)
                                # eco
                                ticket_vjaeco = SeatFlight(ticket_type='vja_eco',
                                                           adult_price=ticket_lst.eco_adult_price,
                                                           child_price=ticket_lst.eco_child_price,
                                                           babe_price=ticket_lst.eco_babe_price,
                                                           adult_ft=ticket_lst.eco_adult_ft,
                                                           child_ft=ticket_lst.eco_child_ft,
                                                           babe_ft=ticket_lst.eco_babe_ft)
                                ticket_vjaeco.set_price(num_adult=self.num_adult,
                                                        num_child=self.num_child,
                                                        num_babe=self.num_infan)
                                # skyboss
                                ticket_vjasky = SeatFlight(ticket_type='vja_sky',
                                                           adult_price=ticket_lst.sky_adult_price,
                                                           child_price=ticket_lst.sky_child_price,
                                                           babe_price=ticket_lst.sky_babe_price,
                                                           adult_ft=ticket_lst.sky_adult_ft,
                                                           child_ft=ticket_lst.sky_child_ft,
                                                           babe_ft=ticket_lst.sky_babe_ft)
                                ticket_vjasky.set_price(num_adult=self.num_adult,
                                                        num_child=self.num_child,
                                                        num_babe=self.num_infan)
                                lst_ticket.append(ticket_vjapromo)
                                lst_ticket.append(ticket_vjaeco)
                                lst_ticket.append(ticket_vjasky)
                            elif flight.carrier == 'jsa':  # jetstar
                                ticket_lst = JSATicket.objects.get(i=flight.ticket)
                                # save
                                ticket_jsasave = SeatFlight(ticket_type='jsa_save',
                                                            adult_price=ticket_lst.save_adult_price,
                                                            child_price=ticket_lst.save_child_price,
                                                            babe_price=ticket_lst.save_babe_price,
                                                            adult_ft=ticket_lst.save_adult_ft,
                                                            child_ft=ticket_lst.save_child_ft,
                                                            babe_ft=ticket_lst.save_babe_ft)
                                ticket_jsasave.set_price(num_adult=self.num_adult,
                                                         num_child=self.num_child,
                                                         num_babe=self.num_infan)
                                # promo
                                ticket_jsaflex = SeatFlight(ticket_type='jsa_flex',
                                                            adult_price=ticket_lst.flex_adult_price,
                                                            child_price=ticket_lst.flex_child_price,
                                                            babe_price=ticket_lst.flex_babe_price,
                                                            adult_ft=ticket_lst.flex_adult_ft,
                                                            child_ft=ticket_lst.flex_child_ft,
                                                            babe_ft=ticket_lst.flex_babe_ft)
                                ticket_jsaflex.set_price(num_adult=self.num_adult,
                                                         num_child=self.num_child,
                                                         num_babe=self.num_infan)
                                # opt
                                ticket_jsaopt = SeatFlight(ticket_type='jsa_opt',
                                                           adult_price=ticket_lst.opt_adult_price,
                                                           child_price=ticket_lst.opt_child_price,
                                                           babe_price=ticket_lst.opt_babe_price,
                                                           adult_ft=ticket_lst.opt_adult_ft,
                                                           child_ft=ticket_lst.opt_child_ft,
                                                           babe_ft=ticket_lst.opt_babe_ft)
                                ticket_jsaopt.set_price(num_adult=self.num_adult,
                                                        num_child=self.num_child,
                                                        num_babe=self.num_infan)
                                lst_ticket.append(ticket_jsasave)
                                lst_ticket.append(ticket_jsaflex)
                                lst_ticket.append(ticket_jsaopt)
                            aresult = ResultFlight(transit=transit)
                            aflight = AFlight()
                            end_port = None
                            # for seat in ticket_lst:
                            aflight.seat_list = lst_ticket
                            aflight.departure_port = flight.departure_port
                            aflight.arrival_port = flight.arrival_port
                            aflight.arrival_name = flight.arrival_port.sname
                            aflight.departure_name = flight.departure_port.sname
                            aflight.departure_time = flight.departure_time
                            aflight.arrival_time = flight.arrival_time
                            aflight.carrier = flight.carrier
                            aflight.flight_code = flight.flight_code
                            aflight.set_min_price()

                            aresult.first_flight = aflight
                            aresult.departure_time = flight.departure_time
                            aresult.arrival_time = flight.arrival_time

                            for second_flight in second_flight_lst:
                                lst_ticket_2 = []
                                if second_flight.carrier == 'vna':
                                    ticket_lst = VNATicket.objects.get(id=second_flight.ticket)
                                    # business flex
                                    ticket_vnabf = SeatFlight(ticket_type='vna_bf',
                                                              adult_price=ticket_lst.bf_adult_price,
                                                              child_price=ticket_lst.bf_child_price,
                                                              babe_price=ticket_lst.bf_babe_price,
                                                              adult_ft=ticket_lst.bf_adult_ft,
                                                              child_ft=ticket_lst.bf_child_ft,
                                                              babe_ft=ticket_lst.bf_babe_ft)
                                    ticket_vnabf.set_price(num_adult=self.num_adult,
                                                           num_child=self.num_child,
                                                           num_babe=self.num_infan)
                                    # business standard
                                    ticket_vnabs = SeatFlight(ticket_type='vna_bs',
                                                              adult_price=ticket_lst.bs_adult_price,
                                                              child_price=ticket_lst.bs_child_price,
                                                              babe_price=ticket_lst.bs_babe_price,
                                                              adult_ft=ticket_lst.bs_adult_ft,
                                                              child_ft=ticket_lst.bs_child_ft,
                                                              babe_ft=ticket_lst.bs_babe_ft)
                                    ticket_vnabs.set_price(num_adult=self.num_adult,
                                                           num_child=self.num_child,
                                                           num_babe=self.num_infan)
                                    # economy flex
                                    ticket_vnaef = SeatFlight(ticket_type='vna_ef',
                                                              adult_price=ticket_lst.ef_adult_price,
                                                              child_price=ticket_lst.ef_child_price,
                                                              babe_price=ticket_lst.ef_babe_price,
                                                              adult_ft=ticket_lst.ef_adult_ft,
                                                              child_ft=ticket_lst.ef_child_ft,
                                                              babe_ft=ticket_lst.ef_babe_ft)
                                    ticket_vnaef.set_price(num_adult=self.num_adult,
                                                           num_child=self.num_child,
                                                           num_babe=self.num_infan)
                                    # economy standard
                                    ticket_vnaes = SeatFlight(ticket_type='vna_es',
                                                              adult_price=ticket_lst.es_adult_price,
                                                              child_price=ticket_lst.es_child_price,
                                                              babe_price=ticket_lst.es_babe_price,
                                                              adult_ft=ticket_lst.es_adult_ft,
                                                              child_ft=ticket_lst.es_child_ft,
                                                              babe_ft=ticket_lst.es_babe_ft)
                                    ticket_vnaes.set_price(num_adult=self.num_adult,
                                                           num_child=self.num_child,
                                                           num_babe=self.num_infan)
                                    # economy save
                                    ticket_vnaesa = SeatFlight(ticket_type='vna_esa',
                                                               adult_price=ticket_lst.esa_adult_price,
                                                               child_price=ticket_lst.esa_child_price,
                                                               babe_price=ticket_lst.esa_babe_price,
                                                               adult_ft=ticket_lst.esa_adult_ft,
                                                               child_ft=ticket_lst.esa_child_ft,
                                                               babe_ft=ticket_lst.esa_babe_ft)
                                    ticket_vnaesa.set_price(num_adult=self.num_adult,
                                                            num_child=self.num_child,
                                                            num_babe=self.num_infan)
                                    # special deal
                                    ticket_vnasd = SeatFlight(ticket_type='vna_sd',
                                                              adult_price=ticket_lst.sd_adult_price,
                                                              child_price=ticket_lst.sd_child_price,
                                                              babe_price=ticket_lst.sd_babe_price,
                                                              adult_ft=ticket_lst.sd_adult_ft,
                                                              child_ft=ticket_lst.sd_child_ft,
                                                              babe_ft=ticket_lst.sd_babe_ft)
                                    ticket_vnasd.set_price(num_adult=self.num_adult,
                                                           num_child=self.num_child,
                                                           num_babe=self.num_infan)

                                    lst_ticket_2.append(ticket_vnabf)
                                    lst_ticket_2.append(ticket_vnabs)
                                    lst_ticket_2.append(ticket_vnaef)
                                    lst_ticket_2.append(ticket_vnaes)
                                    lst_ticket_2.append(ticket_vnaesa)
                                    lst_ticket_2.append(ticket_vnasd)
                                elif second_flight.carrier == 'vja':  # vietjetair
                                    ticket_lst = VJATicket.objects.get(id=second_flight.ticket)
                                    # promo
                                    ticket_vjapromo = SeatFlight(ticket_type='vja_promo',
                                                                 adult_price=ticket_lst.pro_adult_price,
                                                                 child_price=ticket_lst.pro_child_price,
                                                                 babe_price=ticket_lst.pro_babe_price,
                                                                 adult_ft=ticket_lst.pro_adult_ft,
                                                                 child_ft=ticket_lst.pro_child_ft,
                                                                 babe_ft=ticket_lst.pro_babe_ft)
                                    ticket_vjapromo.set_price(num_adult=self.num_adult,
                                                              num_child=self.num_child,
                                                              num_babe=self.num_infan)
                                    # eco
                                    ticket_vjaeco = SeatFlight(ticket_type='vja_eco',
                                                               adult_price=ticket_lst.eco_adult_price,
                                                               child_price=ticket_lst.eco_child_price,
                                                               babe_price=ticket_lst.eco_babe_price,
                                                               adult_ft=ticket_lst.eco_adult_ft,
                                                               child_ft=ticket_lst.eco_child_ft,
                                                               babe_ft=ticket_lst.eco_babe_ft)
                                    ticket_vjaeco.set_price(num_adult=self.num_adult,
                                                            num_child=self.num_child,
                                                            num_babe=self.num_infan)
                                    # skyboss
                                    ticket_vjasky = SeatFlight(ticket_type='vja_sky',
                                                               adult_price=ticket_lst.sky_adult_price,
                                                               child_price=ticket_lst.sky_child_price,
                                                               babe_price=ticket_lst.sky_babe_price,
                                                               adult_ft=ticket_lst.sky_adult_ft,
                                                               child_ft=ticket_lst.sky_child_ft,
                                                               babe_ft=ticket_lst.sky_babe_ft)
                                    ticket_vjasky.set_price(num_adult=self.num_adult,
                                                            num_child=self.num_child,
                                                            num_babe=self.num_infan)
                                    lst_ticket_2.append(ticket_vjapromo)
                                    lst_ticket_2.append(ticket_vjaeco)
                                    lst_ticket_2.append(ticket_vjasky)
                                elif second_flight.carrier == 'jsa':  # jetstar
                                    ticket_lst = JSATicket.objects.get(id=second_flight.ticket)
                                    # save
                                    ticket_jsasave = SeatFlight(ticket_type='jsa_save',
                                                                adult_price=ticket_lst.save_adult_price,
                                                                child_price=ticket_lst.save_child_price,
                                                                babe_price=ticket_lst.save_babe_price,
                                                                adult_ft=ticket_lst.save_adult_ft,
                                                                child_ft=ticket_lst.save_child_ft,
                                                                babe_ft=ticket_lst.save_babe_ft)
                                    ticket_jsasave.set_price(num_adult=self.num_adult,
                                                             num_child=self.num_child,
                                                             num_babe=self.num_infan)
                                    # promo
                                    ticket_jsaflex = SeatFlight(ticket_type='jsa_flex',
                                                                adult_price=ticket_lst.flex_adult_price,
                                                                child_price=ticket_lst.flex_child_price,
                                                                babe_price=ticket_lst.flex_babe_price,
                                                                adult_ft=ticket_lst.flex_adult_ft,
                                                                child_ft=ticket_lst.flex_child_ft,
                                                                babe_ft=ticket_lst.flex_babe_ft)
                                    ticket_jsaflex.set_price(num_adult=self.num_adult,
                                                             num_child=self.num_child,
                                                             num_babe=self.num_infan)
                                    # opt
                                    ticket_jsaopt = SeatFlight(ticket_type='jsa_opt',
                                                               adult_price=ticket_lst.opt_adult_price,
                                                               child_price=ticket_lst.opt_child_price,
                                                               babe_price=ticket_lst.opt_babe_price,
                                                               adult_ft=ticket_lst.opt_adult_ft,
                                                               child_ft=ticket_lst.opt_child_ft,
                                                               babe_ft=ticket_lst.opt_babe_ft)
                                    ticket_jsaopt.set_price(num_adult=self.num_adult,
                                                            num_child=self.num_child,
                                                            num_babe=self.num_infan)
                                    lst_ticket_2.append(ticket_jsasave)
                                    lst_ticket_2.append(ticket_jsaflex)
                                    lst_ticket_2.append(ticket_jsaopt)
                                asflight = AFlight()
                                # for seat in ticket_lst_2:
                                asflight.seat_list = lst_ticket_2
                                asflight.departure_port = second_flight.departure_port
                                asflight.arrival_port = second_flight.arrival_port
                                asflight.arrival_name = second_flight.arrival_port.sname
                                asflight.departure_name = second_flight.departure_port.sname
                                asflight.departure_time = second_flight.departure_time
                                asflight.arrival_time = second_flight.arrival_time
                                asflight.carrier = second_flight.carrier
                                asflight.flight_code = second_flight.flight_code
                                asflight.set_min_price()

                                aresult.end_port = asflight.arrival_name
                                aresult.second_flight.append(asflight)

                            aresult.set_price()

                            self.outward_list.append(aresult)

    def sort_result(self):
        self.outward_list.sort(key=lambda x: x.total_price)

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
