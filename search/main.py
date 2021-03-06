#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .models import Ticket, Carrier, Airport, MiddlePort,\
    VNATicket, VJATicket, JSATicket, \
    IntRegionRoute, IntConnectingMap, IntContinentRoute, \
    IntAirport, IntFlight, IntTicket
from django.db.models import F
from result import Result, Flight
import random
import datetime
import logging
import threading

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] | %(asctime)s -#- %(threadName)-20s : %(message)s',
)


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
        self.total_ticket_fee = num_adult * self.adult_ft + num_child * self.child_ft + num_babe * self.babe_ft
        self.total_price += self.total_ticket_price + self.total_ticket_fee


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

    def get_port_name(self):
        try:
            self.departure_name = IntAirport.objects.get(code=self.departure_port).sname
            self.arrival_name = IntAirport.objects.get(code=self.arrival_port).sname
        except Exception:
            self.departure_name = 'Need to update'
            self.arrival_name = 'Need to update'
            return False
        return True

    def set_min_price(self):
        for seat in self.seat_list:
            if self.total_price_min == 0 or self.total_price_min > seat.total_price:
                self.total_price_min = seat.total_price


class ResultFlight(object):
    def __init__(self, transit=None):
        self.total_price = 0
        self.transit = transit
        self.departure_time = '0000'
        self.arrival_time = '0000'
        self.end_port = None
        self.is_sec = False
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

    def set_int_price(self):
        # get min price of first flight
        self.total_price = self.first_flight.total_price_min
        # get min price of second connect flight
        second_min_price = 0
        for flight in self.second_flight:
            if second_min_price == 0 or flight.total_price < second_min_price:
                second_min_price = flight.total_price
        self.total_price += second_min_price


class ResultIntFlight(object):
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


# ==== some function support for main ====
def get_transit_airport(org, des, stop=1):
    """ origin and destination,
        only use for international
    """
    transit = IntConnectingMap.objects.get(departure_port=org,
                                           arrival_port=des)
    if not transit:
        lst = make_transit(org, des, stop)
        return lst
    if stop == 1:
        if transit.route_transit_once == 0:
            # make transit
            lst = make_transit(org, des, stop, transit)
            return lst
        if transit.route_transit_once == 1:
            return None
        return transit.route_transit_once.split(',')
    if stop == 2:
        if transit.route_transit_twice == 0:
            lst = make_transit(org, des, stop, transit)
            return lst
        if transit.route_transit_twice == 1:
            return None
        return transit.route_transit_twice.split(',')
    # make_transit(org, des, stop)


def make_transit(org, des, stop=1, objects=None):
    """ temp """
    port_org = IntAirport.objects.get(code=org)
    # port_des = IntAirport.objects.get(code=des)
    transit = port_org.router.split(',')
    # make transit 1 stop
    rs_lst_1 = []
    # get list con
    if stop == 1:
        # airport_list = IntAirport.objects.all()
        for item in transit:
            air_port = IntAirport.objects.get(code=item)
            if des in air_port.router:
                rs_lst_1.append(item)
        
        rto = ','.join(rs_lst_1)
        if not rs_lst_1:
            rto = '1'
        if objects:
            objects.route_transit_once = rto
            objects.save()
            return rs_lst_1
        have_direct = False
        transit = port_org.router.split(',')
        if des in transit:
            have_direct = True
        # airport_list = IntAirport.objects.all()
        new_cn = IntConnectingMap(departure_port=org,
                                  arrival_port=des,
                                  have_direct=have_direct,
                                  recommend=False,
                                  route_transit_once=rs_lst_1,
                                  route_transit_twice='0',
                                  date_create=datetime.now(),
                                  is_deleted=0
                                  )
        new_cn.save()
        return rs_lst_1
    # final_result = IntConnectingMap.objects.get(departure_port=org,
    #                                             arrival_port=des)
    rs_lst_2 = []
    for item in transit:
        air_port = IntAirport.objects.get(code=item)
        transit_2 = air_port.router.split(',')
        for place in transit_2:
            if get_transit_airport(place, des):
                rs_lst_2.append(place)
    if objects:
        if rs_lst_2:
            rtt = ','.join(rs_lst_2)
            objects.route_transit_twice=rtt
            objects.save()
            return rs_lst_2
        objects.route_transit_twice='1'
        objects.save()
        return None

    have_direct = False
    transit = port_org.router.split(',')
    if des in transit:
        have_direct = True
    for item in transit:
        air_port = IntAirport.objects.get(code=item)
        if des in air_port.router:
            rs_lst_1.append(item)
    rto = ','.join(rs_lst_1)
    rtt = ','.join(rs_lst_2)
    if not rs_lst_2:
        rtt = '0'
    # airport_list = IntAirport.objects.all()
    new_cn = IntConnectingMap(departure_port=org,
                              arrival_port=des,
                              have_direct=have_direct,
                              recommend=False,
                              route_transit_once=rto,
                              route_transit_twice=rtt,
                              date_create=datetime.now(),
                              is_deleted=0
                              )

    return rs_lst_2


def get_transit_middle(org, des):
    port_org = IntAirport.objects.get(code=org)
    # port_des = IntAirport.objects.get(code=des)

    # make transit 1 stop

    # get list con
    # have_direct = False
    transit = port_org.router.split(',')
    # if des in transit:
        # have_direct = True
    rs_lst = []
    # rs_lst_2 = []
    # airport_list = IntAirport.objects.all()
    for item in transit:
        air_port = IntAirport.objects.get(code=item)
        if des in air_port.router:
            rs_lst.append(item)
    return rs_lst


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

    def greedy_search(self, data=None):
        self.num_adult = data['adult']
        self.num_child = data['child']
        self.num_infan = data['babe']
        self.outward_day = data['go_day']
        self.return_day = data['rt_day']
        self.way = data['way']
        self.dep_port = data['departure']
        self.arr_port = data['arrival']

        self.greedy(self.dep_port, self.arr_port, self.outward_day, 1)

        if self.way == 2:
            self.greedy(self.arr_port, self.dep_port, self.return_day, 2)

    def greedy(self, org, des, date, mode, *args, **kwargs):
        
        td = datetime.timedelta
        
        flight_lst = Ticket.objects.filter(departure_port=org,
                                           arrival_port=des,
                                           departure_time__range=(
                                               datetime.datetime.combine(date, datetime.time.min),
                                               datetime.datetime.combine(date, datetime.time.max))
                                           )
        # TODO --------- search method ---------
        # - OUTWARD
        # Set direct flight result
        if flight_lst:
            for flight in flight_lst:
                # get list ticket suitable with carrier
                # print '---------------', flight.ticket
                lst_ticket = self.get_ticket_list(flight.carrier, flight.ticket)

                # - initial
                # -- ResultFlight: 1 ket qua tra ve
                aresult = ResultFlight()
                # -- Aflight: 1 chuyến bay kết quả trả về
                # Trong trường hợp nà ứng với first flight
                # Second flight is none
                aflight = AFlight()

                # for seat in ticket_lst:
                # set attribute value for a flight
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

                # add first flight to result
                # second flight = none, because this is direct flight
                aresult.first_flight = aflight
                aresult.departure_time = flight.departure_time
                aresult.arrival_time = flight.arrival_time
                aresult.set_price()

                # Thêm kết quả tìm được vào list kết quả
                if mode == 1:
                    self.outward_list.append(aresult)
                else:
                    self.return_list.append(aresult)
        # Lấy hết chuyến bay trong ngày mà xuất phát từ nơi đi
        transit_flight_list = Ticket.objects.filter(departure_port=org,
                                                    departure_time__range=(
                                                        datetime.datetime.combine(date, datetime.time.min),
                                                        datetime.datetime.combine(date, datetime.time.max))
                                                    )
        # Ứng với mỗi chuyến bay tìm được, lấy hết các chuyến bay có xuất phát từ đó
        for flight in transit_flight_list:
            # danh sách các chuyến bay ứng với mỗi chuyến tìm được bên trên
            # print flight.arrival_port.code
            transit_tmp = flight.arrival_port.code
            sec_lst_bf_filter = Ticket.objects.filter(departure_port=transit_tmp,
                                                      departure_time__range=(
                                                          datetime.datetime.combine(date, datetime.time.min),
                                                          datetime.datetime.combine(date, datetime.time.max) + td(hours=36)
                                                          )
                                                      )
            # Nếu không tìm thấy chuyến nào thì chuyển sang duyệt chuyến kế tiếp
            if not sec_lst_bf_filter:
                continue
            # print '-------------------- SOS ---------------------'
            filter_lst = []
            # - initial
            # -- ResultFlight: 1 ket qua tra ve
            # print flight.carrier, flight.ticket
            lst_ticket = self.get_ticket_list(flight.carrier, flight.ticket)
            aresult = ResultFlight(transit=transit_tmp)
            # -- Aflight: 1 chuyến bay kết quả trả về
            # Trong trường hợp nà ứng với first flight
            # Second flight is none
            aflight = AFlight()

            # for seat in ticket_lst:
            # set attribute value for a flight
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

            # Xác định xem có tồn tại list chặng bay tiếp theo hay không
            have_2_lst = False
            # print '-------------------- SOS ---------------------'
            for f in sec_lst_bf_filter:
                # loại các chuyến có điểm đến không phải là đích
                # print f.arrival_port.code
                if transit_tmp == des:
                    continue
                if f.arrival_port != des:
                    continue
                # print '-------------------- SOS ---------------------'
                # loại các chuyến có thời gian cất cánh sớm hơn thời gian chuyến đầu hạ cánh
                if f.departure_time < flight.arrival_time + td(minutes=45):
                    continue
                lst_ticket_2 = self.get_ticket_list(f.carrier, f.ticket)
                asflight = AFlight()
                # for seat in ticket_lst_2:
                asflight.seat_list = lst_ticket_2
                asflight.departure_port = f.departure_port
                asflight.arrival_port = f.arrival_port
                asflight.arrival_name = f.arrival_port.sname
                asflight.departure_name = f.departure_port.sname
                asflight.departure_time = f.departure_time
                asflight.arrival_time = f.arrival_time
                asflight.carrier = f.carrier
                asflight.flight_code = f.flight_code
                asflight.set_min_price()

                aresult.end_port = asflight.arrival_name
                aresult.second_flight.append(asflight)
                have_2_lst = True
            aresult.set_price()

            # Nếu không tồn tại list chặng bay kế tiếp, next
            if not have_2_lst:
                continue

            if mode == 1:
                self.outward_list.append(aresult)
            else:
                self.return_list.append(aresult)
            # self.outward_list.append(aresult)

        return None
    # get ticket in VN
    def get_ticket_list(self, carrier, id):
        return_lst = []
        if carrier == 'vna':
            ticket_lst = VNATicket.objects.get(id=id)
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

            return_lst.append(ticket_vnabf)
            return_lst.append(ticket_vnabs)
            return_lst.append(ticket_vnaef)
            return_lst.append(ticket_vnaes)
            return_lst.append(ticket_vnaesa)
            if ticket_lst.special_deal_num > 0:
                return_lst.append(ticket_vnasd)
        elif carrier == 'vja':
            ticket_lst = VJATicket.objects.get(id=id)
            # promo
            if ticket_lst.promo_num > 0:
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
                return_lst.append(ticket_vjapromo)
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
            return_lst.append(ticket_vjaeco)
            return_lst.append(ticket_vjasky)
        elif carrier == 'jsa':
            ticket_lst = JSATicket.objects.get(id=id)
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
            return_lst.append(ticket_jsasave)
            return_lst.append(ticket_jsaflex)
            return_lst.append(ticket_jsaopt)
        return return_lst

    # get ticket in international
    def get_int_ticket(self, lst_ticket_id):
        result = []
        lst_ticket = lst_ticket_id.split(',')
        for id in lst_ticket:
            tk = IntTicket.objects.get(id=id)
            ticket = SeatFlight(ticket_type=tk.ticket_type,
                                adult_price=tk.price_adult,
                                child_price=tk.price_child,
                                babe_price=tk.price_babe,
                                adult_ft=tk.fee_tax_adult,
                                child_ft=tk.fee_tax_child,
                                babe_ft=tk.fee_tax_babe)
            ticket.set_price(num_adult=self.num_adult,
                             num_child=self.num_child,
                             num_babe=self.num_infan)
            result.append(ticket)
        return result

    # search method
    # the most importance action
    def search(self, data=None):
        self.num_adult = data['adult']
        self.num_child = data['child']
        self.num_infan = data['babe']
        self.outward_day = data['go_day']
        self.return_day = data['rt_day']
        self.way = data['way']
        self.dep_port = data['departure']
        self.arr_port = data['arrival']

        stops = data['stops']

        price_tmp = int(data['maxprice'])
        # print price_tmp 

        if price_tmp == 0:
            max_price = 0
        else:
            max_price = price_tmp/1000

        ohs = data['outhours'].split(',')
        outward_hour = [int(ohs[0]), 24-int(ohs[1])]
        # print outward_hour
        ohs = data['inhours'].split(',')
        return_hour = [int(ohs[0]), 24-int(ohs[1])]

        med_price = 0
        is_med = False

        td = datetime.timedelta
        # num_passenger = self.num_adult + self.num_child + self.num_infan
        transit_list = MiddlePort.objects.get(depart_port=self.dep_port, arrival_port=self.arr_port)

        flight_lst = Ticket.objects.filter(departure_port=self.dep_port,
                                           arrival_port=self.arr_port,
                                           departure_time__range=(
                                               datetime.datetime.combine(self.outward_day, datetime.time.min) + td(hours=outward_hour[0]),
                                               datetime.datetime.combine(self.outward_day, datetime.time.max) - td(hours=outward_hour[1]))
                                           )
        # TODO --------- search method ---------
        # - OUTWARD
        # Set direct flight result
        if flight_lst:
            for flight in flight_lst:
                # get list ticket suitable with carrier
                lst_ticket = self.get_ticket_list(flight.carrier, flight.ticket)

                # - initial
                # -- ResultFlight: 1 ket qua tra ve
                aresult = ResultFlight()
                # -- Aflight: 1 chuyến bay kết quả trả về
                # Trong trường hợp nà ứng với first flight
                # Second flight is none
                aflight = AFlight()

                # for seat in ticket_lst:
                # set attribute value for a flight
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

                if max_price != 0 and aflight.total_price_min > max_price:
                    continue

                # add first flight to result
                # second flight = none, because this is direct flight
                aresult.first_flight = aflight
                aresult.departure_time = flight.departure_time
                aresult.arrival_time = flight.arrival_time
                aresult.set_price()

                # Thêm kết quả tìm được vào list kết quả
                self.outward_list.append(aresult)
        # check transit list
        # *note : now we just check if flight trip is exist in database
        if len(self.outward_list):
            is_med = True
            if max_price != 0:
                med_price = max_price
            else:
                for item in self.outward_list:
                    med_price += item.total_price
                med_price /= len(self.outward_list)
                print med_price
                med_price = med_price*2
            tmp_price = 0
        else:
            if max_price != 0:
                is_med = True
                med_price = max_price
        if transit_list and stops == 0:
            # get transit port,which is stored in db at string, then split them into list.
            lst_transit_port = transit_list.middle_port.split(',')
            for transit in lst_transit_port:
                first_flight_lst = Ticket.objects.filter(departure_port=self.dep_port,
                                                         arrival_port=transit,
                                                         departure_time__range=(
                                                             datetime.datetime.combine(self.outward_day,
                                                                                       datetime.time.min) + td(hours=outward_hour[0]),
                                                             datetime.datetime.combine(self.outward_day,
                                                                                       datetime.time.max) - td(hours=outward_hour[1]))
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
                            lst_ticket = self.get_ticket_list(flight.carrier, flight.ticket)
                            aresult = ResultFlight(transit=transit)
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

                            if is_med:
                                tmp_price = aflight.total_price_min
                                if aflight.total_price_min > med_price:
                                    continue

                            aresult.first_flight = aflight
                            aresult.departure_time = flight.departure_time
                            aresult.arrival_time = flight.arrival_time

                            if is_med:
                                count_2_flight = 0

                            for second_flight in second_flight_lst:
                                lst_ticket_2 = self.get_ticket_list(second_flight.carrier, second_flight.ticket)

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

                                if is_med:
                                    if tmp_price + asflight.total_price_min > med_price:
                                      continue 

                                    count_2_flight += 1
                                aresult.end_port = asflight.arrival_name
                                aresult.second_flight.append(asflight)
                            if is_med:
                                if count_2_flight == 0:
                                    continue
                            aresult.set_price()

                            self.outward_list.append(aresult)

        # - RETURN
        if self.way == 2:
            transit_list = MiddlePort.objects.get(depart_port=self.arr_port, arrival_port=self.dep_port)

            flight_lst = Ticket.objects.filter(departure_port=self.arr_port,
                                               arrival_port=self.dep_port,
                                               departure_time__range=(
                                                   datetime.datetime.combine(self.return_day, datetime.time.min) + td(hours=return_hour[0]),
                                                   datetime.datetime.combine(self.return_day, datetime.time.max) - td(hours=return_hour[1]))
                                               )
            # direct return flight
            is_med = False
            if flight_lst:
                for flight in flight_lst:
                    lst_ticket = self.get_ticket_list(flight.carrier, flight.ticket)
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

                    if max_price != 0 and aflight.total_price_min > max_price:
                        continue

                    aresult.first_flight = aflight
                    aresult.departure_time = flight.departure_time
                    aresult.arrival_time = flight.arrival_time
                    aresult.set_price()

                    # Thêm kết quả tìm được vào list kết quả
                    self.return_list.append(aresult)
            # if len(self.return_list):
            #     is_med = True
            #     for item in self.outward_list:
            #         med_price += item.total_price
            #     med_price /= len(self.return_list)
            #     print med_price
            #     med_price = med_price*2
            #     tmp_price = 0
            if len(self.return_list):
                is_med = True
                if max_price != 0:
                    med_price = max_price
                else:
                    for item in self.return_list:
                        med_price += item.total_price
                    med_price /= len(self.return_list)
                    print med_price
                    med_price = med_price*2
                tmp_price = 0
            else:
                if max_price != 0:
                    is_med = True
                    med_price = max_price
            # transit return flight
            if transit_list and stops == 0:
                lst_transit_port = transit_list.middle_port.split(',')
                for transit in lst_transit_port:
                    first_flight_lst = Ticket.objects.filter(departure_port=self.arr_port,
                                                             arrival_port=transit,
                                                             departure_time__range=(
                                                                 datetime.datetime.combine(self.return_day,
                                                                                           datetime.time.min) + td(hours=return_hour[0]),
                                                                 datetime.datetime.combine(self.return_day,
                                                                                           datetime.time.max) - td(hours=return_hour[1]))
                                                             )
                    if first_flight_lst:
                        for flight in first_flight_lst:
                            second_flight_lst = Ticket.objects.filter(departure_port=transit,
                                                                      arrival_port=self.dep_port,
                                                                      departure_time__range=(
                                                                          flight.arrival_time + td(hours=0, minutes=45),
                                                                          flight.arrival_time + td(hours=5, minutes=15)
                                                                      )
                                                                      )
                            if second_flight_lst:
                                lst_ticket = self.get_ticket_list(flight.carrier, flight.ticket)
                                aresult = ResultFlight(transit=transit)
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

                                if is_med:
                                    tmp_price = aflight.total_price_min
                                    if aflight.total_price_min > med_price:
                                        continue

                                    count_2_flight = 0

                                aresult.first_flight = aflight
                                aresult.departure_time = flight.departure_time
                                aresult.arrival_time = flight.arrival_time

                                for second_flight in second_flight_lst:
                                    lst_ticket_2 = self.get_ticket_list(second_flight.carrier, second_flight.ticket)

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

                                    if is_med:
                                        if tmp_price + asflight.total_price_min > med_price:
                                            continue 
                                        count_2_flight += 1

                                    aresult.end_port = asflight.arrival_name
                                    aresult.second_flight.append(asflight)

                                if is_med:
                                    if count_2_flight == 0:
                                        continue
                                aresult.set_price()

                                self.return_list.append(aresult)

        # sort result by price
        self.sort_result()

    ###################################################################################################################
    ###################################################################################################################

    def int_search(self, data):
        self.num_adult = data['adult']
        self.num_child = data['child']
        self.num_infan = data['babe']
        self.outward_day = data['go_day']
        self.return_day = data['rt_day']
        self.way = data['way']
        self.dep_port = data['departure']
        self.arr_port = data['arrival']
        td = datetime.timedelta
        # num_passenger = self.num_adult + self.num_child + self.num_infan
        transit_list = IntConnectingMap.objects.get(departure_port=self.dep_port, arrival_port=self.arr_port)
        # Get direct flight
        flight_lst = IntFlight.objects.filter(departure_port=self.dep_port,
                                              arrival_port=self.arr_port,
                                              departure_time__range=(
                                                  datetime.datetime.combine(self.outward_day, datetime.time.min),
                                                  datetime.datetime.combine(self.outward_day, datetime.time.max))
                                              )
        # ----- TODO : make seach with 2 transit -----
        # - OUTWARD
        # set direct flight
        if flight_lst:
            for flight in flight_lst:
                # get list ticket suitable with carrier
                lst_ticket = self.get_int_ticket(flight.ticket)
                aresult = ResultFlight()
                aflight = AFlight()

                # for seat in ticket_lst:
                aflight.seat_list = lst_ticket
                aflight.departure_port = flight.departure_port
                aflight.arrival_port = flight.arrival_port
                # aflight.arrival_name = flight.arrival_port.sname
                # aflight.departure_name = flight.departure_port.sname
                # replace with function get name
                aflight.get_port_name()
                aflight.departure_time = flight.departure_time
                aflight.arrival_time = flight.arrival_time
                aflight.carrier = flight.carrier
                aflight.flight_code = flight.flight_code
                aflight.set_min_price()

                # because this is direct flight so it not have second flight list
                aresult.first_flight = aflight
                aresult.departure_time = flight.departure_time
                aresult.arrival_time = flight.arrival_time
                aresult.set_price()

                # Thêm kết quả tìm được vào list kết quả
                # each flight after calculation are added to outward_list
                self.outward_list.append(aresult)
        # set transit flight
        # typical a flight would have this format
        # flight:
        #   first:  A flight
        #   sec:
        #       [
        #           {
        #               first: A flight
        #               sec:    [
        #                           {
        #                               first: A flight
        #                               sec: None
        #                           }
        #                       ]
        #           }
        #       ]

        if transit_list:
            # - 1 transit
            # get transit port then split into list type.
            # nothing much different from domestic search
            lst_transit_port = transit_list.route_transit_once.split(',')
            for transit in lst_transit_port:
                # get first flight
                first_flight_lst = IntFlight.objects.filter(departure_port=self.dep_port,
                                                            arrival_port=transit,
                                                            departure_time__range=(
                                                                datetime.datetime.combine(self.outward_day,
                                                                                          datetime.time.min),
                                                                datetime.datetime.combine(self.outward_day,
                                                                                          datetime.time.max))
                                                            )
                # check if flight list not none
                if not first_flight_lst:
                    # break
                    continue
                # loop for each flight in flight list
                for flight in first_flight_lst:
                    insert = False
                    # in each flight in flight list
                    # get it's continuous flight
                    second_flight_lst = IntFlight.objects.filter(departure_port=transit,
                                                                 arrival_port=self.arr_port,
                                                                 departure_time__range=(
                                                                     flight.arrival_time + td(hours=0, minutes=45),
                                                                     flight.arrival_time + td(hours=5, minutes=15)
                                                                 )
                                                                 )
                    # check sec flight list not none
                    # if it is none -> next flight
                    # else do something
                    if not second_flight_lst:
                        continue
                    # get ticket list of flight
                    lst_ticket = self.get_int_ticket(flight.ticket)
                    aresult = ResultFlight(transit=transit)
                    aflight = AFlight()
                    # for seat in ticket_lst:
                    aflight.seat_list = lst_ticket
                    aflight.departure_port = flight.departure_port
                    aflight.arrival_port = flight.arrival_port
                    # aflight.arrival_name = flight.arrival_port.sname
                    # aflight.departure_name = flight.departure_port.sname
                    # replace with fuction get name
                    aflight.get_port_name()
                    aflight.departure_time = flight.departure_time
                    aflight.arrival_time = flight.arrival_time
                    aflight.carrier = flight.carrier
                    aflight.flight_code = flight.flight_code
                    aflight.set_min_price()

                    aresult.first_flight = aflight
                    aresult.departure_time = flight.departure_time
                    aresult.arrival_time = flight.arrival_time

                    for second_flight in second_flight_lst:
                        lst_ticket = self.get_int_ticket(second_flight.ticket)

                        asflight = AFlight()
                        # for seat in ticket_lst_2:
                        asflight.seat_list = lst_ticket
                        asflight.departure_port = second_flight.departure_port
                        asflight.arrival_port = second_flight.arrival_port
                        # asflight.arrival_name = second_flight.arrival_port.sname
                        # asflight.departure_name = second_flight.departure_port.sname
                        # replace with function get name
                        asflight.get_port_name()
                        asflight.departure_time = second_flight.departure_time
                        asflight.arrival_time = second_flight.arrival_time
                        asflight.carrier = second_flight.carrier
                        asflight.flight_code = second_flight.flight_code
                        asflight.set_min_price()

                        aresult.end_port = asflight.arrival_name
                        aresult.second_flight.append(asflight)
                        insert = True

                    aresult.set_price()
                    if insert:
                        self.outward_list.append(aresult)
            # - 2 transit
            # -- TODO - make 2 transit
            # Summarized:
            # E.g. A -> B -> C -> D
            # Basically separate into 2 part
            # Part 1: direct flight from A to B
            # Part 2: transit flight form B to D

            # Retrieve transit first list
            lst_transit_first = transit_list.route_transit_twice.split(',')
            for transit in lst_transit_first:
                # Make part 1
                # Direct flight from A to B (B form transit first list)
                first_flight_lst = IntFlight.objects.filter(departure_port=self.dep_port,
                                                            arrival_port=transit,
                                                            departure_time__range=(
                                                                datetime.datetime.combine(self.outward_day,
                                                                                          datetime.time.min),
                                                                datetime.datetime.combine(self.outward_day,
                                                                                          datetime.time.max))
                                                            )
                # TODO check arrival_port at below
                # if not have flight from A to B, so continue on next airport
                if not first_flight_lst:
                    continue

                for flight in first_flight_lst:
                    insert = False
                    # something wrong ...
                    # fix in 3 .. 2 .. 1 .. done
                    # retrieve ticket for first flight - b2c
                    lst_ticket = self.get_int_ticket(flight.ticket)

                    # A result flight consist of:
                    # One flight from A 2 B
                    # A list from B to C
                    # and each list form C 2 D
                    a_result_flight = ResultFlight(transit=transit)

                    # A flight from A 2 B
                    a_flight = AFlight()

                    a_flight.seat_list = lst_ticket
                    a_flight.departure_port = flight.departure_port
                    a_flight.arrival_port = flight.arrival_port
                    # a_flight.arrival_name = flight.arrival_port.sname
                    # a_flight.departure_name = flight.departure_port.sname
                    # replace both line with get sname function
                    a_flight.get_port_name()
                    a_flight.departure_time = flight.departure_time
                    a_flight.arrival_time = flight.arrival_time
                    a_flight.carrier = flight.carrier
                    a_flight.flight_code = flight.flight_code
                    a_flight.set_min_price()

                    # add flight to a_result
                    a_result_flight.is_sec = True
                    a_result_flight.first_flight = a_flight
                    a_result_flight.departure_time = flight.departure_time
                    a_result_flight.arrival_time = flight.arrival_time

                    # Make part 2

                    # Get transit form B to D
                    lst_transit_sec = IntConnectingMap.objects.get(departure_port=transit,
                                                                   arrival_port=self.arr_port) \
                        .route_transit_once.split(',')
                    # For each transit in transit list:
                    # Making a search for it
                    for sec_transit in lst_transit_sec:
                        # transit is B
                        # sec_transit is C
                        first_flight_of_sec = IntFlight.objects.filter(departure_port=transit,
                                                                       arrival_port=sec_transit,
                                                                       departure_time__range=(
                                                                           flight.arrival_time + td(hours=0,
                                                                                                    minutes=45),
                                                                           flight.arrival_time + td(hours=5,
                                                                                                    minutes=15)
                                                                       ))
                        # skip to next transit if there are haven't part 1
                        if not first_flight_of_sec:
                            continue

                        # loop in first flight list
                        for sec_flight in first_flight_of_sec:

                            # checking if exist flight from C 2 D
                            sec_flight_of_sec = IntFlight.objects.filter(departure_port=sec_transit,
                                                                         arrival_port=self.arr_port,
                                                                         departure_time__range=(
                                                                             sec_flight.arrival_time + td(hours=0,
                                                                                                          minutes=45),
                                                                             sec_flight.arrival_time + td(hours=5,
                                                                                                          minutes=15)
                                                                         ))
                            if not sec_flight_of_sec:
                                continue

                            # retrieve ticket

                            lst_ticket = self.get_int_ticket(sec_flight.ticket)
                            
                            # create new result flight for part 2: B2D
                            a_sec_result_flight = ResultFlight(transit=sec_transit)
    
                            # A flight from B 2 C
                            a_sec_flight = AFlight()
    
                            a_sec_flight.seat_list = lst_ticket
                            a_sec_flight.departure_port = sec_flight.departure_port
                            a_sec_flight.arrival_port = sec_flight.arrival_port
                            # a_sec_flight.arrival_name = flight.arrival_port.sname
                            # a_sec_flight.departure_name = flight.departure_port.sname
                            # replace both line with get sname function
                            a_sec_flight.get_port_name()
                            a_sec_flight.departure_time = sec_flight.departure_time
                            a_sec_flight.arrival_time = sec_flight.arrival_time
                            a_sec_flight.carrier = sec_flight.carrier
                            a_sec_flight.flight_code = sec_flight.flight_code
                            a_sec_flight.set_min_price()
    
                            # add flight to a_result
                            a_sec_result_flight.first_flight = a_sec_flight
                            a_sec_result_flight.departure_time = sec_flight.departure_time
                            a_sec_result_flight.arrival_time = sec_flight.arrival_time

                            # loop for second flight : c2d
                            # sec_transit = C
                            # transit = B
                            # dep = A
                            # arrival = D
                            for sec_sec_flight in sec_flight_of_sec:
                                lst_ticket = self.get_int_ticket(sec_sec_flight.ticket)

                                # A flight from B 2 C
                                a_sec_flight = AFlight()

                                a_sec_flight.seat_list = lst_ticket
                                a_sec_flight.departure_port = sec_sec_flight.departure_port
                                a_sec_flight.arrival_port = sec_sec_flight.arrival_port
                                # a_sec_flight.arrival_name = flight.arrival_port.sname
                                # a_sec_flight.departure_name = flight.departure_port.sname
                                # replace both line with get sname function
                                a_sec_flight.get_port_name()
                                a_sec_flight.departure_time = sec_sec_flight.departure_time
                                a_sec_flight.arrival_time = sec_sec_flight.arrival_time
                                a_sec_flight.carrier = sec_sec_flight.carrier
                                a_sec_flight.flight_code = sec_sec_flight.flight_code
                                a_sec_flight.set_min_price()

                                # add flight to a_result
                                a_sec_result_flight.end_port = a_sec_flight.arrival_name
                                a_sec_result_flight.second_flight.append(a_sec_flight)

                            a_sec_result_flight.set_price()
                            # add part 2 to part 1 as
                            a_result_flight.end_port = a_sec_result_flight.end_port
                            a_result_flight.second_flight.append(a_sec_result_flight)
                            insert = True

                    # set price after do search for 1 flight in first flight list
                    a_result_flight.set_int_price()
                    # add result to outward list
                    if insert:
                        self.outward_list.append(a_result_flight)
                    # ----------------- * - * - * ----------------- #
                    # --------------------------------------------- #
                    # --------------------------------------------- #
                    # --------------------------------------------- #

        # - RETURN
        if self.way != 2:
            self.sort_result()
            return False
        # --------------------------------------------------------------------------------------------------------------
        # set direct flight
        # just a reverse of outward, change position of arrival port and departure port
        transit_list = IntConnectingMap.objects.get(departure_port=self.arr_port, arrival_port=self.dep_port)
        # direct flight return
        flight_lst = IntFlight.objects.filter(departure_port=self.arr_port,
                                              arrival_port=self.dep_port,
                                              departure_time__range=(
                                                  datetime.datetime.combine(self.return_day, datetime.time.min),
                                                  datetime.datetime.combine(self.return_day, datetime.time.max)
                                              ))
        # make direct return
        if flight_lst:
            for flight in flight_lst:
                # get list ticket suitable with carrier
                lst_ticket = self.get_int_ticket(flight.ticket)
                aresult = ResultFlight()
                aflight = AFlight()

                # for seat in ticket_lst:
                aflight.seat_list = lst_ticket
                aflight.departure_port = flight.departure_port
                aflight.arrival_port = flight.arrival_port
                # aflight.arrival_name = flight.arrival_port.sname
                # aflight.departure_name = flight.departure_port.sname
                # replace with function get name
                aflight.get_port_name()
                aflight.departure_time = flight.departure_time
                aflight.arrival_time = flight.arrival_time
                aflight.carrier = flight.carrier
                aflight.flight_code = flight.flight_code
                aflight.set_min_price()

                # because this is direct flight so it not have second flight list
                aresult.first_flight = aflight
                aresult.departure_time = flight.departure_time
                aresult.arrival_time = flight.arrival_time
                aresult.set_price()

                # Thêm kết quả tìm được vào list kết quả - RETURN -
                # each flight after calculation are added to outward_list
                self.return_list.append(aresult)
        # set transit flight
        # typical a flight would have this format
        # flight:
        #   first:  A flight
        #   sec:
        #       [
        #           {
        #               first: A flight
        #               sec:    [
        #                           {
        #                               first: A flight
        #                               sec: None
        #                           }
        #                       ]
        #           }
        #       ]

        # transit return
        # may be no need if here, hm.
        if transit_list:
            # > 1 stop transit
            # get transit port then split into list type.
            # nothing much different from domestic search
            lst_transit_port = transit_list.route_transit_once.split(',')
            for transit in lst_transit_port:
                # get first flight
                # from arrival port to transit stop
                first_flight_lst = IntFlight.objects.filter(departure_port=self.arr_port,
                                                            arrival_port=transit,
                                                            departure_time__range=(
                                                                datetime.datetime.combine(self.return_day,
                                                                                          datetime.time.min),
                                                                datetime.datetime.combine(self.return_day,
                                                                                          datetime.time.max))
                                                            )
                # check if flight list not none
                if not first_flight_lst:
                    # break
                    # wrong, move to next transit stop if current stop have empty flight list
                    continue
                # loop for each flight in flight list
                for flight in first_flight_lst:
                    insert = False
                    # for each flight in flight list
                    # get it's continuous flight
                    second_flight_lst = IntFlight.objects.filter(departure_port=transit,
                                                                 arrival_port=self.dep_port,
                                                                 departure_time__range=(
                                                                     flight.arrival_time + td(hours=0, minutes=45),
                                                                     flight.arrival_time + td(hours=5, minutes=15)
                                                                 )
                                                                 )
                    # check sec flight list not none
                    # if it is none -> next flight
                    # else do something
                    if not second_flight_lst:
                        continue
                    # get ticket list of flight
                    lst_ticket = self.get_int_ticket(flight.ticket)
                    aresult = ResultFlight(transit=transit)
                    aflight = AFlight()
                    # for seat in ticket_lst:
                    aflight.seat_list = lst_ticket
                    aflight.departure_port = flight.departure_port
                    aflight.arrival_port = flight.arrival_port
                    # aflight.arrival_name = flight.arrival_port.sname
                    # aflight.departure_name = flight.departure_port.sname
                    # replace with fuction get name
                    aflight.get_port_name()
                    aflight.departure_time = flight.departure_time
                    aflight.arrival_time = flight.arrival_time
                    aflight.carrier = flight.carrier
                    aflight.flight_code = flight.flight_code
                    aflight.set_min_price()

                    aresult.first_flight = aflight
                    aresult.departure_time = flight.departure_time
                    aresult.arrival_time = flight.arrival_time

                    for second_flight in second_flight_lst:
                        lst_ticket = self.get_int_ticket(second_flight.ticket)

                        asflight = AFlight()
                        # for seat in ticket_lst_2:
                        asflight.seat_list = lst_ticket
                        asflight.departure_port = second_flight.departure_port
                        asflight.arrival_port = second_flight.arrival_port
                        # asflight.arrival_name = second_flight.arrival_port.sname
                        # asflight.departure_name = second_flight.departure_port.sname
                        # replace with function get name
                        asflight.get_port_name()
                        asflight.departure_time = second_flight.departure_time
                        asflight.arrival_time = second_flight.arrival_time
                        asflight.carrier = second_flight.carrier
                        asflight.flight_code = second_flight.flight_code
                        asflight.set_min_price()

                        aresult.end_port = asflight.arrival_name
                        aresult.second_flight.append(asflight)
                        insert = True

                    aresult.set_price()
                    if insert:
                        self.return_list.append(aresult)
            # - 2 transit
            # -- TODO - make 2 transit
            # Summarized:
            # E.g. A -> B -> C -> D
            # Basically separate into 2 part
            # Part 1: direct flight from A to B
            # Part 2: transit flight form B to D

            # Retrieve transit first list
            lst_transit_first = transit_list.route_transit_twice.split(',')
            for transit in lst_transit_first:
                # Make part 1
                # Direct flight from A to B (B form transit first list)
                first_flight_lst = IntFlight.objects.filter(departure_port=self.arr_port,
                                                            arrival_port=transit,
                                                            departure_time__range=(
                                                                datetime.datetime.combine(self.return_day,
                                                                                          datetime.time.min),
                                                                datetime.datetime.combine(self.return_day,
                                                                                          datetime.time.max))
                                                            )
                # TODO check arrival_port at below
                # if not have flight from A to B, so continue on next airport
                if not first_flight_lst:
                    continue

                for flight in first_flight_lst:
                    insert = False
                    # something wrong ...
                    # fix in 3 .. 2 .. 1 .. done
                    # retrieve ticket for first flight - b2c
                    lst_ticket = self.get_int_ticket(flight.ticket)

                    # A result flight consist of:
                    # One flight from A 2 B
                    # A list from B to C
                    # and each list form C 2 D
                    a_result_flight = ResultFlight()

                    # A flight from A 2 B
                    a_flight = AFlight()

                    a_flight.seat_list = lst_ticket
                    a_flight.departure_port = flight.departure_port
                    a_flight.arrival_port = flight.arrival_port
                    # a_flight.arrival_name = flight.arrival_port.sname
                    # a_flight.departure_name = flight.departure_port.sname
                    # replace both line with get sname function
                    a_flight.get_port_name()
                    a_flight.departure_time = flight.departure_time
                    a_flight.arrival_time = flight.arrival_time
                    a_flight.carrier = flight.carrier
                    a_flight.flight_code = flight.flight_code
                    a_flight.set_min_price()

                    # add flight to a_result
                    a_result_flight.first_flight = a_flight
                    a_result_flight.departure_time = flight.departure_time
                    a_result_flight.arrival_time = flight.arrival_time

                    # Make part 2

                    # Get transit form B to D
                    lst_transit_sec = IntConnectingMap.objects.get(departure_port=transit,
                                                                   arrival_port=self.dep_port) \
                        .route_transit_once.split(',')
                    # For each transit in transit list:
                    # Making a search for it
                    for sec_transit in lst_transit_sec:
                        # transit is B
                        # sec_transit is C
                        first_flight_of_sec = IntFlight.objects.filter(departure_port=transit,
                                                                       arrival_port=sec_transit,
                                                                       departure_time__range=(
                                                                           flight.arrival_time + td(hours=0,
                                                                                                    minutes=45),
                                                                           flight.arrival_time + td(hours=5,
                                                                                                    minutes=15)
                                                                       ))
                        # skip to next transit if there are haven't part 1
                        if not first_flight_of_sec:
                            continue

                        # loop in first flight list
                        for sec_flight in first_flight_of_sec:

                            # checking if exist flight from C 2 D
                            sec_flight_of_sec = IntFlight.objects.filter(departure_port=sec_transit,
                                                                         arrival_port=self.dep_port,
                                                                         departure_time__range=(
                                                                             sec_flight.arrival_time + td(hours=0,
                                                                                                          minutes=45),
                                                                             sec_flight.arrival_time + td(hours=5,
                                                                                                          minutes=15)
                                                                         ))
                            if not sec_flight_of_sec:
                                continue

                            # retrieve ticket

                            lst_ticket = self.get_int_ticket(sec_flight.ticket)

                            # create new result flight for part 2: B2D
                            a_sec_result_flight = ResultFlight(transit=sec_transit)

                            # A flight from B 2 C
                            a_sec_flight = AFlight()

                            a_sec_flight.seat_list = lst_ticket
                            a_sec_flight.departure_port = sec_flight.departure_port
                            a_sec_flight.arrival_port = sec_flight.arrival_port
                            # a_sec_flight.arrival_name = flight.arrival_port.sname
                            # a_sec_flight.departure_name = flight.departure_port.sname
                            # replace both line with get sname function
                            a_sec_flight.get_port_name()
                            a_sec_flight.departure_time = sec_flight.departure_time
                            a_sec_flight.arrival_time = sec_flight.arrival_time
                            a_sec_flight.carrier = sec_flight.carrier
                            a_sec_flight.flight_code = sec_flight.flight_code
                            a_sec_flight.set_min_price()

                            # add flight to a_result
                            a_sec_result_flight.first_flight = a_sec_flight
                            a_sec_result_flight.departure_time = sec_flight.departure_time
                            a_sec_result_flight.arrival_time = sec_flight.arrival_time

                            # loop for second flight : c2d
                            # sec_transit = C
                            # transit = B
                            # dep = A
                            # arrival = D
                            for sec_sec_flight in sec_flight_of_sec:
                                lst_ticket = self.get_int_ticket(sec_sec_flight.ticket)

                                # A flight from B 2 C
                                a_sec_flight = AFlight()

                                a_sec_flight.seat_list = lst_ticket
                                a_sec_flight.departure_port = a_sec_flight.departure_port
                                a_sec_flight.arrival_port = a_sec_flight.arrival_port
                                # a_sec_flight.arrival_name = flight.arrival_port.sname
                                # a_sec_flight.departure_name = flight.departure_port.sname
                                # replace both line with get sname function
                                a_sec_flight.get_port_name()
                                a_sec_flight.departure_time = a_sec_flight.departure_time
                                a_sec_flight.arrival_time = a_sec_flight.arrival_time
                                a_sec_flight.carrier = a_sec_flight.carrier
                                a_sec_flight.flight_code = a_sec_flight.flight_code
                                a_sec_flight.set_min_price()

                                # add flight to a_result
                                a_sec_result_flight.end_port = a_sec_flight.arrival_name
                                a_sec_result_flight.second_flight.append(a_sec_flight)

                            a_sec_result_flight.set_price()
                            # add part 2 to part 1 as
                            a_result_flight.end_port = a_sec_result_flight.end_port
                            a_result_flight.second_flight.append(a_sec_result_flight)
                            insert = True

                    # set price after do search for 1 flight in first flight list
                    a_result_flight.set_int_price()
                    # add result to outward list
                    if insert:
                        self.return_list.append(a_result_flight)
                        # ----------------- * - * - * ----------------- #
                        # --------------------------------------------- #
                        # --------------------------------------------- #
                        # --------------------------------------------- #
        self.sort_result()

    def sort_result(self):
        self.outward_list = sorted(self.outward_list, key=lambda x: x.total_price)
        self.return_list = sorted(self.return_list, key=lambda x: x.total_price)

    @staticmethod
    def get_by_date(date):
        lst = Ticket.object.filter(departure_time__exact=date)
        return lst

################################################################################################
#
#                         ------- THE INTERNATIONAL -------
#
################################################################################################