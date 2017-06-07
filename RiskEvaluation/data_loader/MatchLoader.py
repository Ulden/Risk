#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re

from RiskEvaluation.models import Link


class MatchLoader:
    def __init__(self,matchcsv):
        self.csv = matchcsv

    def parse(self):
        with open(self.csv,'r') as csv:
            lines = csv.readlines()
            for line in lines:
                line, number = re.subn(r'\"\"', '\"0\"', line)
                splited = re.split(r'[\s\,\"]+', line)
                splited.remove('')
                link = Link.objects.get(link_id = splited[0][6:-1])
