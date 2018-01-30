#!/bin/python
# coding:utf8

import os
import time
import json
import signal
import datetime
import traceback

import collections

import BusDataRequest


def g_append_one_line_to_file(filename, text):
    dir = os.path.dirname(filename)
    if not os.path.exists(dir):
        os.mkdir(dir)

    if isinstance(text, unicode):
        text = text.encode('utf8')

    with open(filename, 'a+') as log_file:
        log_file.write(text)
        log_file.write('\n')


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
        self.current_time = 0
        self.__last_station = {}

    def tick(self):
        request_interval = self.config['request_interval']
        line_info_list = self.config['line_info_list']

        # 每隔一定时间尝试请求数据
        if self.last_request_time + request_interval < self.current_time:
            for line_info in line_info_list:
                self.__request_line_info(line_info)
            self.last_request_time = self.current_time

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
            print repr(e)
            print traceback.print_exc()

    def __consume_data(self, line_info, data):
        for bus_info in data['data']:
            cur_datetime = datetime.datetime.fromtimestamp(self.current_time)
            bus_id = bus_info['BusNumber']
            current_station = bus_info['CurrentStation']
            str_datetime = cur_datetime.strftime('%Y-%m-%d %H:%M:%S')
            str_date = cur_datetime.strftime('%Y%m%d')

            # 如果巴士的最后站点发生变化，则记录
            if bus_id not in self.__last_station or self.__last_station[bus_id] != current_station:
                self.__last_station[bus_id] = current_station

                filename_param = {
                    'date': str_date,
                    'bus_id': bus_id
                }
                filename_param.update(line_info)

                filename = os.path.join(self.config['output_dir'], self.config['output_filename']) % filename_param
                text = ','.join([str_datetime, line_info['line_name'], bus_id, current_station])

                g_append_one_line_to_file(filename, text)

    def run(self):

        self.is_running = True

        while self.is_running:
            self.current_time = time.time()
            self.tick()
            time.sleep(0.1)


def g_convert(data):
    if isinstance(data, unicode):
        return data.encode('utf8')
    elif isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(g_convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(g_convert, data))
    else:
        return data


if __name__ == '__main__':
    CONFIG_PATH = './config.json'
    config = {}
    with open(CONFIG_PATH, 'r') as f:
        config = g_convert(json.load(f))

    collector = BusDataCollector(config)


    def signal_handler(signal, frame):
        print 'Ctrl C'
        collector.is_running = False


    signal.signal(signal.SIGINT, signal_handler)

    collector.run()

    print 'Stop'
