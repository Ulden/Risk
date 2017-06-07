#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.db import models


class SE_node(models.Model):
    grid = models.CharField(max_length = 255)
    node_id = models.CharField(max_length = 30, primary_key = True)
    lon = models.FloatField()
    lat = models.FloatField()
    links_id = models.TextField()


class Link(models.Model):
    map_id = models.CharField(max_length = 30)
    link_id = models.CharField(max_length = 30, primary_key = True)
    Kind_num = models.CharField(max_length = 255)
    Kind = models.CharField(max_length = 30)
    Width = models.CharField(max_length = 255)
    Direction = models.CharField(max_length = 255)
    Toll = models.CharField(max_length = 255)
    Const_St = models.CharField(max_length = 255)
    UndConCRID = models.CharField(max_length = 255)
    SnodeID = models.ForeignKey(SE_node, on_delete = models.CASCADE, related_name = 'SNode')
    EnodeID = models.ForeignKey(SE_node, on_delete = models.CASCADE, related_name = 'ENode')
    FuncClass = models.CharField(max_length = 255)
    Length = models.CharField(max_length = 255)
    DetailCity = models.CharField(max_length = 255)
    Through = models.CharField(max_length = 255)
    UnThruCRID = models.CharField(max_length = 13)
    Ownership = models.CharField(max_length = 255)
    Road_Cond = models.CharField(max_length = 255)
    Special = models.CharField(max_length = 255)
    AdminCodeL = models.CharField(max_length = 30)
    AdminCodeR = models.CharField(max_length = 30)
    Uflag = models.CharField(max_length = 255)
    OnewayCRID = models.CharField(max_length = 30)
    AccessCRID = models.CharField(max_length = 30)
    SpeedClass = models.CharField(max_length = 255)
    LaneNumS2E = models.CharField(max_length = 30)
    LaneNumE2S = models.CharField(max_length = 30)
    LaneNum = models.CharField(max_length = 255)
    Vehcl_Type = models.CharField(max_length = 255)
    Elevated = models.CharField(max_length = 255)
    Structure = models.CharField(max_length = 255)
    UseFeeCRID = models.CharField(max_length = 30)
    UseFeeType = models.CharField(max_length = 255)
    SpdLmtS2E = models.CharField(max_length = 30)
    SpdLmtE2S = models.CharField(max_length = 30)
    SpdSrcS2E = models.CharField(max_length = 255)
    SpdSrcE2S = models.CharField(max_length = 255)
    DC_Type = models.CharField(max_length = 255)
    NoPassCRID = models.CharField(max_length = 30)
    OutBanCRID = models.CharField(max_length = 30)
    NumBanCRID = models.CharField(max_length = 30)
    ParkFlag = models.CharField(max_length = 255)
    points = models.TextField()


class POI(models.Model):
    grid = models.CharField(max_length = 255)
    poi_id = models.AutoField(primary_key = True)
    kind = models.CharField(max_length = 255)
    telephone = models.CharField(max_length = 255)
    chain_code = models.CharField(max_length = 255)
    zip_code = models.CharField(max_length = 255)
    admin_code = models.CharField(max_length = 255)
    vadmin_code = models.CharField(max_length = 255)
    lon = models.CharField(max_length = 255)
    lat = models.CharField(max_length = 255)
    importance = models.CharField(max_length = 255)
    prior_auth = models.CharField(max_length = 255)
    link_id = models.ForeignKey(Link, on_delete = models.CASCADE)
    side = models.CharField(max_length = 255)
    pid = models.CharField(max_length = 255)  # 旧id
    tel_type = models.CharField(max_length = 255)
    poi_flag = models.CharField(max_length = 255)  # POI 分级


class TrafficSign(models.Model):
    grid_id = models.CharField(max_length = 255)
    in_link_id = models.ForeignKey(Link, on_delete = models.CASCADE)
    node_id = models.ForeignKey(SE_node, on_delete = models.CASCADE)
    type = models.CharField(max_length = 255)
    valid_dist = models.CharField(max_length = 255)
    pre_dist = models.CharField(max_length = 255)
    cr_id = models.CharField(max_length = 255)


class attributes_relation(models.Model):
    attribute_a = models.CharField(max_length = 255)
    attribute_b = models.CharField(max_length = 255)
    value = models.IntegerField(default = 0)


class link_attributes(models.Model):
    link = models.ForeignKey(Link,on_delete = models.CASCADE)
    # attribute = models.CharField(max_length = 255)
    # value = models.FloatField()
    # time = models.DateTimeField()
    # time_related = models.BooleanField()
    trrafic_sign = models.CharField(max_length = 255)
    lane_num = models.CharField(max_length = 255)
    lane_width = models.CharField(max_length = 255)
    mixed_traffic = models.CharField(max_length = 255)
    speed_limit = models.CharField(max_length = 255)
    radius = models.CharField(max_length = 255)
    poi_num = models.IntegerField(default = 0)
    poi_importance = models.FloatField(default = 0.0)


class Matched_GPS(models.Model):
    record_id = models.AutoField(primary_key = True)
    vehicle_id = models.CharField(max_length = 255)
    link_id = models.ForeignKey(Link, on_delete = models.CASCADE)
    matched_num = models.IntegerField()
    in_time = models.DateTimeField()
    out_time = models.DateTimeField()

