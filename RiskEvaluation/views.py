#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import math
import random

from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from RiskEvaluation.data_loader import load_data
from RiskEvaluation.evaluation.ahp import AHP
from RiskEvaluation.evaluation.topsis import Topsis
from RiskEvaluation.models import Link, link_attributes, attributes_relation, Matched_GPS


def index(request):
    return render(request, 'potential.html', {'title': '潜在风险'})


def real_risk(request):
    return render(request, 'risk.html', {'title': '实际风险'})


def weight_assign(request):
    road_tags = ['width', 'num', 'mixed', 'radius', 'sign', 'speed']
    vehicle_tags = ['pass', 'weight', 'cargo']
    poi_tags = ['poi', 'importance']

    name = {'width': '车道宽度', 'num': '车道数量', 'mixed': '混合交通', 'radius': '道路曲率', 'sign': '交通标志', 'speed': '限速范围',
            'pass': '通行量', 'weight': '平均载重', 'cargo': '货物种类', 'poi': 'POI数量', 'importance': 'POI重要性'}

    return render(request, 'weight.html',
                  {'road_tags': road_tags, 'vehicle_tags': vehicle_tags, 'poi_tags': poi_tags, 'name': name,
                   'title': '指标权重'})


def potential_data(request):
    result = []
    links = Link.objects.filter(Kind__regex = '\d*00...+')  # map_id = 595751
    for link in links:
        value = link.matched_gps_set.count()
        coords = []
        for point_str in re.split(r'[\,]', link.points):
            try:
                lon_lat = re.split(r'[\s\,\t]+', point_str)
                coords.append(gps_trans(float(lon_lat[0]), float(lon_lat[1])))
            except:
                pass
        result.append({'coords': coords, 'value': value, 'name': link.link_id})
    return JsonResponse(result, safe = False)


def realrisk_data(request):
    result = []
    n = random.randint(1, 2000)
    links = Link.objects.filter(Kind__regex = '\d*00...+')[n:n+3000]
    for link in links:
        value = random.randint(1,12)
        coords = []
        for point_str in re.split(r'[\,]', link.points):
            try:
                lon_lat = re.split(r'[\s\,\t]+', point_str)
                coords.append(gps_trans(float(lon_lat[0]), float(lon_lat[1])))
            except:
                pass
        result.append({'coords': coords, 'value': value, 'name': link.link_id})
    return JsonResponse(result, safe = False)



def data(request):
    ahp = AHP()
    weight = ahp.weight()
    matrix = []
    attribs = {}
    for branch in weight:
        for key in weight[branch]:
            attribs[key] = weight[branch][key]


def attributes_data(request, link):
    attributes = link_attributes.objects.filter(link__link_id = link)
    # res.append({
    #     'traffic_sign': attribute.trrafic_sign,
    #     'lane_num':attribute.lane_num,
    #     'lane_width':attribute.lane_width,
    #     'mixed_traffic':attribute.mixed_traffic,
    #     'speed_limit':attribute.speed_limit,
    #     'radius':attribute.radius
    # })
    random.randint(1, 20)
    res = [[random.randint(1, 20) for i in range(6)]]
    return JsonResponse(res, safe = False)


def loader(request):
    load_data()
    return HttpResponse("Loading Data")


def update_weights(request):
    if request.method == 'POST':
        content = request.POST
        list = {key: content[key] for key in content.keys() if key != 'csrfmiddlewaretoken'}
        for key in list.keys():
            splited = re.split(r'[\_]', key)
            A = splited[0]
            B = splited[1]
            try:
                item = attributes_relation.objects.get(attribute_a = A, attribute_b = B)
                item.value = list[key]
            except attributes_relation.DoesNotExist:
                item = attributes_relation(attribute_a = A, attribute_b = B, value = list[key])
            item.save()
    return redirect(reverse(weight_assign))


def calculate_weight(request):
    ahp = AHP()
    weight = ahp.weight()
    value = []
    for branch in weight:
        attribs = []
        for key in weight[branch]:
            attribs.append({'value': float(weight[branch][key]), 'name': key})
        value.append(attribs)
    return JsonResponse(value, safe = False)


def calculate(request):
    ahp = AHP()
    weight = ahp.weight()
    matrix = []
    attribs = {}
    for branch in weight:
        for key in weight[branch]:
            attribs[key] = weight[branch][key]

    for link in Link.objects.all():
        vector = [link_attributes.objects.get(link = link, attribute = attrib).value for attrib in attribs.keys()]
        matrix.append(vector)
    topsis = Topsis(matrix, weight, [link.link_id for link in Link.objects.all()])
    topsis.normalize()
    topsis.weight_assign()
    result = topsis.ranked()
    print(result)
    # TODO:将计算的指标结果存入数据库
    return redirect(reverse(index))


def gps_trans(x, y):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * x_pi)
    bd_lon = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return bd_lon, bd_lat


def trans(x, y):
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    x = x - 0.0065
    y = y - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lon = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return gg_lon, gg_lat
