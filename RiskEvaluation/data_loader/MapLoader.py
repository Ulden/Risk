#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
from datetime import datetime
from multiprocessing.pool import Pool

from RiskEvaluation.models import Link, SE_node, POI, TrafficSign, Matched_GPS


class MapLoader:
    def __init__(self, R_mid_file, R_mif_file, N_mid_file, N_mif_file):
        """
        Load Map into database from MapInfo format data
        :param R_mid_file: Road information (Link)
        :param R_mif_file: Points on roads (Odinary Points)
        :param N_mid_file: Node infomation (SNode & ENode)
        :param N_mif_file: Lon & Lat of nodes
        """
        self.r_mid = R_mid_file
        self.r_mif = R_mif_file
        self.n_mid = N_mid_file
        self.n_mif = N_mif_file

    def node_parse(self):
        with open(self.n_mid, 'r') as mid_file:
            with open(self.n_mif, 'r') as mif_file:
                points = mid_file.readlines()
                raw = mif_file.readlines()
                latlons = []
                for line in raw:
                    if re.match(r'^Point\s.+\s.+\d$', line):
                        latlons.append(line)
                for point, latlon in zip(points, latlons):
                    point, number = re.subn(r'\"\"', '\"0\"', point)
                    point_split = re.split(r'[\s\,\"]+', point)
                    latlon_split = re.split(r'[\s]+', latlon)
                    point_split.remove('')
                    node = SE_node(lon = latlon_split[1], lat = latlon_split[2], node_id = point_split[1],
                                       grid = point_split[0], links_id = point_split[12])
                    node.save()

                    print('node saved')

    def link_parse(self):
        with open(self.r_mid, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line, number = re.subn(r'\"\"', '\"0\"', line)
                splited = re.split(r'[\s\,\"]+', line)
                splited.remove('')
                snode = SE_node.objects.get(node_id=splited[9])
                enode = SE_node.objects.get(node_id=splited[10])
                link = Link(map_id = splited[0], link_id = splited[1], Kind_num = splited[2], Kind = splited[3],
                                   Width = splited[4], Direction = splited[5], Toll = splited[6], Const_St = splited[7],
                                   UndConCRID = splited[8], SnodeID = snode, EnodeID = enode,
                                   FuncClass = splited[11], Length = splited[12], DetailCity = splited[13],
                                   Through = splited[14], UnThruCRID = splited[15], Ownership = splited[16],
                                   Road_Cond = splited[17], Special = splited[18], AdminCodeL = splited[19],
                                   AdminCodeR = splited[20], Uflag = splited[21], OnewayCRID = splited[22],
                                   AccessCRID = splited[23], SpeedClass = splited[24], LaneNumS2E = splited[25],
                                   LaneNumE2S = splited[26], LaneNum = splited[27], Vehcl_Type = splited[28],
                                   Elevated = splited[29], Structure = splited[30], UseFeeCRID = splited[31],
                                   UseFeeType = splited[32], SpdLmtS2E = splited[33], SpdLmtE2S = splited[34],
                                   SpdSrcS2E = splited[35], SpdSrcE2S = splited[36], DC_Type = splited[37],
                                   NoPassCRID = splited[38], OutBanCRID = splited[39], NumBanCRID = splited[40],
                                   ParkFlag = splited[41])
                link.save()

                print('line saved')

    def ordpoint_parse(self):
        with open("/Users/wangzhaoyi/PycharmProjects/Risk/RiskEvaluation/static/link_ordpoint.csv",'r') as ord:
            lines = ord.readlines()
            for line in lines:
                link_id = int(line[6:14])
                points = line[15:]
                link = Link.objects.get(link_id = link_id)
                link.points = points
                link.save()

    def poi_parse(self):
        with open('/Users/wangzhaoyi/Desktop/TianJin/tianjin/index/POItianjin.mid', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line, number = re.subn(r'\"\"', '\"0\"', line)
                splited = re.split(r'[\s\,\"]+', line)
                splited.remove('')
                link = Link.objects.get(link_id=splited[12])
                poi = POI(grid = splited[0], kind = splited[1], zip_code = splited[2], telephone = splited[3],
                                 admin_code = splited[4], lon = splited[5], lat = splited[6], poi_id = splited[7],
                                 importance = splited[8], vadmin_code = splited[9], chain_code = splited[10],
                                 prior_auth = splited[11], link_id = link, side = splited[13], pid = splited[14],
                                 tel_type = splited[15], poi_flag = splited[16])
                poi.save()

                print('poi saved')

    def load_single_record(self,item):
        line, number = re.subn(r'\"\"', '\"0\"', item)
        splited = re.split(r'[\s\,\"]+', line)
        splited.remove('')
        link = Link.objects.get(link_id = splited[1])
        node = SE_node.objects.get(node_id = splited[2])
        sign = TrafficSign(grid_id = splited[0], in_link_id = link, node_id = node, type = splited[3],
                           valid_dist = splited[4], pre_dist = splited[5], cr_id = splited[6])
        sign.save()

    def trafficsigh_parse(self):
        file_path = '/Users/wangzhaoyi/Desktop/TianJin/tianjin/road/TrfcSigntianjin.mid'
        with open(file_path) as file:
            lines = file.readlines()
            p = Pool()
            p.map(self.load_single_record, lines)

    def matched_parse(self):
        match_dir = '/Users/wangzhaoyi/Desktop/TianJin/tianjin/TianjinResult/'
        for file in os.listdir(match_dir):
            matched_file = match_dir+file
            with open(matched_file,'r') as f:
                try:
                    lines = f.readlines()
                    time_format = '%Y%m%d%H%M%S'
                    list = [Matched_GPS(vehicle_id = line.split(',')[0],link_id =Link.objects.get(link_id = int(line.split(',')[1][6:])),matched_num = line.split(',')[2],in_time = datetime.strptime(line.split(',')[7],time_format),out_time = datetime.strptime(line.split(',')[8][:-1],time_format)) for line in lines]
                    Matched_GPS.objects.bulk_create(list)
                except:
                    pass
