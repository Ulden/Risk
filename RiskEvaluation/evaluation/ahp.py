#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np

from RiskEvaluation.models import attributes_relation


class AHPMatrix:
    def __init__(self, matrix, index):
        self.A_matrix = np.array(matrix)
        self.O_matrix = np.array(matrix)
        self.C_matrix = np.array(matrix)
        self.index = index

    def parse_matrix(self):
        matrix = self.C_matrix
        n = max(matrix.shape)
        for i in range(0, n):
            for j in range(0, n):
                sum = 0
                for k in range(0, n):
                    sum += matrix[i][k] + matrix[k][j]
                self.O_matrix[i][j] = float(sum) / n

        for i in range(0, n):
            for j in range(0, n):
                self.A_matrix[i][j] = np.exp(self.O_matrix[i][j])

    def weight(self):
        self.parse_matrix()
        a, b = np.linalg.eig(self.A_matrix)
        for i in range(0, a.size):
            if a[i] == a.max():
                raw_array = b[:, i]
        raw_array /= raw_array.sum()
        result = {}
        for i in range(0, a.size):
            result[self.index[i]] = raw_array[i]
        return result


class AHP:
    def __init__(self):
        self.road_tags = ['width', 'num', 'mixed', 'radius', 'sign', 'speed']
        # self.vehicle_tags = ['pass', 'weight', 'cargo']
        self.poi_tags = ['poi', 'importance']
        self.total_tags = ['road', 'poi']
        matrix_road = []
        # matrix_vehicle = []
        matrix_poi = []
        matrix_total = [[0, 0], [0, 0]]
        for f_tag in self.road_tags:
            tmp_array = []
            for b_tag in self.road_tags:
                tmp = attributes_relation.objects.get(attribute_a = f_tag, attribute_b = b_tag)
                tmp_array.append(tmp.value)
            matrix_road.append(tmp_array)
        # for f_tag in self.vehicle_tags:
        #     tmp_array = []
        #     for b_tag in self.vehicle_tags:
        #         tmp = attributes_relation.objects.get(attribute_a = f_tag, attribute_b = b_tag)
        #         tmp_array.append(tmp.value)
        #     matrix_vehicle.append(tmp_array)
        for f_tag in self.poi_tags:
            tmp_array = []
            for b_tag in self.poi_tags:
                tmp = attributes_relation.objects.get(attribute_a = f_tag, attribute_b = b_tag)
                tmp_array.append(tmp.value)
            matrix_poi.append(tmp_array)

        self.m_road = AHPMatrix(matrix_road, self.road_tags)
        # self.m_vehicle = AHPMatrix(matrix_vehicle, self.vehicle_tags)
        self.m_poi = AHPMatrix(matrix_poi, self.poi_tags)
        self.m_total = AHPMatrix(matrix_total, self.total_tags)

    def weight(self):
        w_road = self.m_road.weight()
        # w_vehicle = self.m_vehicle.weight()
        w_poi = self.m_poi.weight()
        w_total = self.m_total.weight()
        result = {'road': w_road, 'poi': w_poi}

        for tag in result.keys():
            for item in result[tag]:
                result[tag][item] *= w_total[tag]
        return result
