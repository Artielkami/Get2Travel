#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response, render, redirect
from .models import Ticket, Airport
from .forms import Search
from .main import Main
from dataAdapter import DataAdapter
# import pytz
# Create your views here.


# this one predecate
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


def about_page(request):
    return render(request, 'search/about.html')


def contact_page(request):
    return render(request, 'search/contact.html')


def domestic(request):
    if request.GET.get('departure'):
        main = Main()
        search_form = Search(request.GET)
        # print('run domestic')
        if search_form.is_valid():
            # print ('form is_valid')
            clean_data = search_form.cleaned_data
            quantity = {'adult': clean_data['adult'],
                        'child': clean_data['child'],
                        'babe': clean_data['babe']}
            dates = {'go': clean_data['go_day'],
                     'back': clean_data['rt_day']}
            places = {'dep': Airport.objects.get(code=clean_data['departure']).sname,
                      'arr': Airport.objects.get(code=clean_data['arrival']).sname}
            lst_result = main.get_ticket(dep=clean_data['departure'],
                                         arr=clean_data['arrival'],
                                         way=clean_data['way'],
                                         stop=clean_data['stops'],
                                         ttype=clean_data['ttype'],
                                         go_day=clean_data['go_day'],
                                         rt_day=clean_data['rt_day']
                                         )
            sform = {'departure': clean_data['departure'],
                     'arrival': clean_data['arrival'],
                     'way': clean_data['way'],
                     'stop': clean_data['stops'],
                     'go_day': clean_data['go_day'],
                     'rt_day': clean_data['rt_day'],
                     'ttype': clean_data['ttype']}
            if lst_result:
                if clean_data['stops'] == 2:
                    return render(request,
                                  'search/index.html',
                                  {
                                      'item_list': lst_result,
                                      # 'rt_list': rt_result,
                                      'rs_type': 'stop',
                                      'places': places,
                                      'dates': dates,
                                      'sform': sform,
                                      'quan': quantity
                                  })
                elif clean_data['way'] == 2:
                    rt_result = main.get_ticket(dep=clean_data['arrival'],
                                                arr=clean_data['departure'],
                                                way=clean_data['way'],
                                                stop=clean_data['stops'],
                                                ttype=clean_data['ttype'],
                                                go_day=clean_data['rt_day'],
                                                rt_day=clean_data['rt_day']
                                                )
                    return render(request,
                                  'search/index.html',
                                  {
                                      'item_list': lst_result,
                                      'rt_list': rt_result,
                                      'places': places,
                                      'dates': dates,
                                      'sform': sform,
                                      'quan': quantity
                                  })
                return render(request,
                              'search/index.html',
                              {
                                  'item_list': lst_result,
                                  'sform': sform,
                                  'dates': dates,
                                  'places': places,
                                  'quan': quantity
                              })
            else:
                return_msg = 'Không tìm thấy kết quả'
                return render(request,
                              'search/index.html',
                              {
                                  'sform': sform,
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
                          'is_search': search
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
