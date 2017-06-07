#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),

    url(r'^$', views.index, name = 'potential'),
    url(r'^risk$', views.real_risk, name = 'risk'),
    url(r'^weight$',views.weight_assign,name = 'weight_assign'),

    url(r'^data/potential$', views.potential_data, name = 'potential_risk'),
    url(r'^data/realrisk$',views.realrisk_data, name = 'real_risk'),
    url(r'^data/weights$',views.calculate_weight,name = 'get_weights'),

    url(r'^data/load$', views.loader, name = 'load_data'),
    url(r'^data/updateweights$', views.update_weights, name = 'update_weights'),

    url(r'^data/attributes(?P<link>\d+)$', views.attributes_data, name = 'attribute_data'),

    url(r'^caculate$', views.calculate, name = 'caculate'),
    url(r'^caculate_weight$', views.calculate_weight, name = 'caculate_weight'),
]
