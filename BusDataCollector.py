#!/bin/python
# coding:utf8

import os
import time
import datetime
import BusDataRequest


def g_append_one_line_to_file(filename, text):
    # TODO 完善函数
    print filename, text


class BusDataCollector:
    default_config = {
        'output_dir': './output',
        'output_filename': '%(line_name)s-%(direction)s-%(date)s-%(bus_id)s.csv',
        'request_interval': 60,
        'line_info_list': [
            # {
            #     'line_name': '3',
            #     'line_id': '7cb4cfe6-fb21-43da-abe3-ba5ee9cfea5e',
            #     'from_station': '金鼎工业园',
            #     'direction': '1'
            # }
        ]
    }

    def __init__(self, config):
        self.config = self.default_config
        self.config.update(config)

        self.is_running = False
        self.last_request_time = 0
        self.__current_time = 0
        self.__last_station = {}

    def __tick(self):
        request_interval = self.config['request_interval']
        line_info_list = self.config['line_info_list']

        # 每隔一定时间尝试请求数据
        if self.last_request_time + request_interval < self.__current_time:
            for line_info in line_info_list:
                self.__request_line_info(line_info)
            self.last_request_time = self.__current_time

    def __request_line_info(self, line_info):
        request = BusDataRequest.BusInfoOnRoad(line_info['line_name'], line_info['from_station'])

        try:
            request.fetch_data()

            if request.last_exception:
                raise request.last_exception

            if request.data_fetched:
                # 成功取到数据，检查并写入
                self.__consume_data(line_info, request.data)
        except Exception as e:
            print e.message

    def __consume_data(self, line_info, data):
        for bus_info in data['data']:
            cur_datetime = datetime.datetime.fromtimestamp(self.__current_time)
            bus_id = bus_info['BusNumber']
            current_station = bus_info['CurrentStation']
            str_datetime = cur_datetime.strftime('%Y-%m-%d %H:%M:%S')
            str_date = cur_datetime.strftime('%Y%m%d')

            # 如果巴士的最后站点发生变化，则记录
            if bus_id not in self.__last_station or self.__last_station[bus_id] != current_station:
                self.__last_station[bus_id] = current_station

                filename = os.path.join(self.config['output_dir'], self.config['output_filename']) % {
                    'date': str_date,
                    'bus_id': bus_id
                }.update(line_info)
                text = ','.join([str_datetime, line_info['line_name'], bus_id, current_station])

                g_append_one_line_to_file(filename, text)

    def run(self):

        self.is_running = True

        while self.is_running:
            self.__current_time = time.time()
            self.__tick()
            time.sleep(0.1)
