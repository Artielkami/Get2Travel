from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    # ex: /search/
    url(r'^$', views.domestic, name='index'),
    url(r'^updateRoutes/$', views.update_routes, name='update_routes'),
    url(r'^about/$', views.about_page, name='about'),
    url(r'^contact/$', views.contact_page, name='contact'),
    url(r'^delete/$', views.del_all_ticket, name='delete'),
    url(r'^domestic/$', views.domestic, name='domestic'),
    url(r'^insert/$', views.insert_db_ticket, name='insert_db_ticket')

    # ex: /polls/5/
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]

urlpatterns += staticfiles_urlpatterns()
