#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response, render, redirect
from .models import Ticket
from .forms import Search
from .main import Main
# import pytz
# Create your views here.


def index(request):
    if request.method == 'GET':
        print 'search'
        # main = Main()
        search_form = Search(request.GET)
        # lst_result = main.get_by_date(search_form.go_date)[:10]
        lst_result = Ticket.objects.all()
        return render(request,
                      'demo/index.html',
                      {
                          'item_list': lst_result
                      })
    else:
        print 'fail'
        ticket_list = Ticket.objects.order_by('-day')
        template = loader.get_template('demo/UI.html')
        context = {
            'item_list': ticket_list,
        }

        # output = ', '.join([q.question_text for q in latest_question_list])
        # return HttpResponse(output)
        return HttpResponse(template.render(context, request))


def domestic(request):
    depart = request.GET.get('departure_port')
    print depart
    if depart:
        main = Main()
        search_form = Search(request.GET)
        if search_form.is_valid():
            clean_data = search_form.cleaned_data
            lst_result = main.get_by_date(clean_data.go_date)[:5]
            return render(request,
                          'demo/index.html',
                          {
                              'item_list': lst_result
                          })
        else:
            return redirect('/domestic')
    else:
        lst_result = Ticket.objects.order_by('price')[:6]
        return render(request,
                      'demo/index.html',
                      {
                          'item_list': lst_result
                      })


def insert_db_ticket(request):
    main = Main()
    main.make_some_db()
    return redirect('/domestic')
