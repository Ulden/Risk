#!/usr/bin/env python
# -*- coding:utf-8 -*-
from multiprocessing.pool import Pool

from RiskEvaluation.data_loader.MapLoader import MapLoader


def load_data():
    maploader = MapLoader(R_mid_file = '/Users/wangzhaoyi/PycharmProjects/Risk/RiskEvaluation/static/Rtianjin.mid', R_mif_file = '/Users/wangzhaoyi/PycharmProjects/Risk/RiskEvaluation/static/Rtianjin.mif',
                          N_mid_file = '/Users/wangzhaoyi/PycharmProjects/Risk/RiskEvaluation/static/Ntianjin.mid', N_mif_file = '/Users/wangzhaoyi/PycharmProjects/Risk/RiskEvaluation/static/Ntianjin.mif')
    # maploader.node_parse()
    # maploader.link_parse()
    # maploader.ordinarypoint_parse()
    # maploader.poi_parse()
    # maploader.trafficsigh_parse()
    maploader.ordpoint_parse()
    maploader.matched_parse()
