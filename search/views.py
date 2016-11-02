#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response, render, redirect
from .models import Ticket, Airport
from .forms import Search
from .main import Main
from dataAdapter import DataAdapter
import simplejson
# import pytz
# Create your views here.
INDEX_PAGE = 'search/index.html'
DOMESTIC_SEARCH = 'search/domestic'
INT_SEARCH = 'search/domestic'


# this one not use anymore
def index(request):
    if request.method == 'GET':
        print 'search'
        # main = Main()
        search_form = Search(request.GET)
        # lst_result = main.get_by_date(search_form.go_date)[:10]
        lst_result = Ticket.objects.all()
        return render(request,
                      'search/index.html',
                      {
                          'item_list': lst_result
                      })
    else:
        print 'fail'
        ticket_list = Ticket.objects.order_by('-day')
        template = loader.get_template('search/UI.html')
        context = {
            'item_list': ticket_list,
        }

        # output = ', '.join([q.question_text for q in latest_question_list])
        # return HttpResponse(output)
        return HttpResponse(template.render(context, request))


def int_search(request):
    basic_data = {
        'action_link': 'search/int_search',
        'domestic_search': DOMESTIC_SEARCH,
        'int_search': INT_SEARCH,
        'is_int_search': True
    }
    if request.GET.get('international_search'):

        return None
    return render(request,
                  INDEX_PAGE,
                  {
                      'base_data': basic_data
                  })


def about_page(request):
    return render(request, 'search/about.html')


def contact_page(request):
    return render(request, 'search/contact.html')


def domestic(request):
    """ Domestic search """
    # some basic key value link action link for form, etc.
    basic_data = {
        'action_link': 'search/domestic',
        'domestic_search': DOMESTIC_SEARCH,
        'int_search': INT_SEARCH
    }

    if request.GET.get('departure'):
        main = Main()
        search_form = Search(request.GET)
        if search_form.is_valid():
            clean_data = search_form.cleaned_data
            quantity = {'adult': clean_data['adult'],
                        'child': clean_data['child'],
                        'babe': clean_data['babe']}
            dates = {'go': clean_data['go_day'],
                     'back': clean_data['rt_day']}
            # get name of airport
            places = {'dep': Airport.objects.get(code=clean_data['departure']).sname,
                      'arr': Airport.objects.get(code=clean_data['arrival']).sname}

            main.search(clean_data)
            sform = {'departure': clean_data['departure'],
                     'arrival': clean_data['arrival'],
                     'way': clean_data['way'],
                     'stop': clean_data['stops'],
                     'go_day': clean_data['go_day'],
                     'rt_day': clean_data['rt_day'],
                     'ttype': clean_data['ttype']}
            if main.outward_list:
                return render(request,
                              'search/index.html',
                              {
                                  'outward_list': main.outward_list,
                                  'return_list': main.return_list,
                                  'sform': sform,
                                  'dates': dates,
                                  'places': places,
                                  'quan': quantity,
                                  'base_data': basic_data
                              })
            else:
                return_msg = 'Không tìm thấy kết quả.'
                return render(request,
                              'search/index.html',
                              {
                                  'sform': sform,
                                  'quan': quantity,
                                  'base_data': basic_data,
                                  'return_msg': return_msg
                              })
        else:
            return redirect('/domestic')
    else:
        # lst_result = Ticket.objects.order_by('price')[:6]
        lst_result = None
        search = None
        return render(request,
                      'search/index.html',
                      {
                          'item_list': lst_result,
                          'is_search': search,
                          'base_data': basic_data
                      })


def update_routes(request):
    DataAdapter.make_routes()
    return redirect('/domestic')


def insert_db_ticket(request):
    DataAdapter.make_some_db()
    return redirect('/domestic')


def del_all_ticket(request):
    DataAdapter.del_all_ticket()
    return redirect('/domestic')
