#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Flight(object):
    """flight ticket, use for 'Result' """
    def __init__(self):
        # price and fee, tax
        self.total_price = 0  # total_price = fee + ticket
        self.total_fee = 0
        self.total_ticket_price = 0
        self.adult_price = 0
        self.adult_fee = 0
        self.child_price = 0
        self.child_fee = 0
        self.infan_price = 0
        self.infan_fee = 0
        self.bonus_fee = 0
        # flight infor
        self.dep_port = None
        self.arr_port = None
        self.dep_date = None
        self.dep_time = None
        self.arr_date = None
        self.arr_time = None
        self.carrier = None
        self.ticket_type = None
        self.flight_code = None

    def set_price(self, num_adult, num_child, num_infan):
        self.total_ticket_price = num_adult*self.adult_price +\
            num_child*self.child_price +\
            num_infan*self.infan_price
        self.total_fee = self.bonus_fee*(num_infan + num_child + num_adult) +\
            num_adult*self.adult_fee +\
            num_child*self.child_fee +\
            num_infan*self.infan_fee
        self.total_price = self.total_ticket_price + self.total_fee


class Result(object):
    """Định dạng kết quả tìm kiếm"""
    def __init__(self):
        # gia tong ca hai luot tring chuyen
        self.total_price = 0
        self.dep_time = None
        self.dep_date = None
        self.arr_time = None
        self.arr_date = None
        self.type = 0  # bay truc tiep hoac gian tiep
        self.len = 0  # thoi gian bay
        self.first_flight = None
        self.second_flight = None

    def set_price(self):
        self.total_price = self.first_flight.total_price + \
                           self.second_flight.total_price

    def sort(self, sort_method):
        return None
