#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np


class Topsis:
    def __init__(self, matrix, weight, index):
        self.matrix = np.array(matrix)
        self.r_matrix = np.array(matrix)
        self.w_matrix = np.array(matrix)
        self.index = index
        self.weight = {}
        for branch in weight:
            for key in weight[branch]:
                self.weight[key] = weight[branch][key]

    def normalize(self):
        for i in range(0, self.matrix.shape[0]):
            for j in range(0, self.matrix.shape[1]):
                sum = 0
                for k in range(0, self.matrix.shape[0]):
                    sum += self.matrix[k][j] ** 2
                self.r_matrix[i][j] = self.matrix[i][j] / np.sqrt(sum)

    def weight_assign(self):
        weight = [self.weight[key] for key in self.weight.keys()]
        for i in range(0, self.matrix.shape[0]):
            for j in range(0, self.matrix.shape[1]):
                self.w_matrix[i][j] = self.matrix[i][j] * weight[j]

    def ranked(self):
        anti_ideal = np.min(self.w_matrix, axis = 0)
        ideal = np.max(self.w_matrix, axis = 0)

        d_better = np.sqrt(np.sum(np.power(self.w_matrix - ideal, 2), axis = 1))
        d_worst = np.sqrt(np.sum(np.power(self.w_matrix - anti_ideal, 2), axis = 1))

        closeness = d_worst / (d_better + d_worst)

        return zip(self.index,closeness)
