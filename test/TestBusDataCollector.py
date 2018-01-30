#!/bin/python
# coding: utf8

import json

import time

from BusDataCollector import BusDataCollector
from test.TestBase import TestWithMock


class TestBusDataCollector(TestWithMock):

    def test_run(self):
        """测试基础功能"""
        collector = BusDataCollector({
            'output_dir': './output',
            'output_filename': '%(line_name)s-%(direction)s-%(date)s-%(bus_id)s.csv',
            'request_interval': 60,
            'line_info_list': [
                {
                    'line_name': '3',
                    'line_id': '7cb4cfe6-fb21-43da-abe3-ba5ee9cfea5e',
                    'from_station': u'金鼎工业园',
                    'direction': '1'
                }
            ]
        })

        self.mock_http_get.return_value = json.dumps({
            'data': [
                {
                    'BusNumber': '粤C18309',
                    'CurrentStation': '九洲城',
                    'LastPosition': '5'
                }
            ]
        })

        collector.current_time = time.mktime((2018, 1, 23, 12, 34, 56, 0, 0, 0))
        collector.tick()

        self.assertEqual(self.mock_append_one_line_to_file.get_args(0), u'./output/3-1-20180123-粤C18309.csv')

        line = self.mock_append_one_line_to_file.get_args(1)
        data = line.split(',')
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], u'2018-01-23 12:34:56')
        self.assertEqual(data[1], u'3')
        self.assertEqual(data[2], u'粤C18309')
        self.assertEqual(data[3], u'九洲城')
