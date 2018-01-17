#!/bin/python
# coding:utf8


class BusDataCollector:

    default_config = {
        'output_dir': './output',
        'output_filename': '%(line_name)s-%(direction)s-%(date)s-%(car_id)s.csv',
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

