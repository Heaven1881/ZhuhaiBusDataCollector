#!/bin/python
# coding:utf8
import collections
import json
import logging
import signal
import sys
import os
from logging.handlers import RotatingFileHandler

from BusDataCollector import BusDataCollector


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
    FORMAT = '%(asctime)s - %(levelname)s - %(module)s: %(message)s'
    log_formatter = logging.Formatter(FORMAT)

    # 在开始前，初始化日志逻辑

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(log_formatter)
    logger.addHandler(stdout_handler)

    # 读取配置
    CONFIG_PATH = './config.json'
    config = {}
    with open(CONFIG_PATH, 'r') as f:
        config = g_convert(json.load(f))

    # 如果指定了日志文件，则将日志写入文件
    if 'logfile' in config:
        filename = config.get('logfile')
        logger.removeHandler(stdout_handler)

        dir_name = os.path.dirname(filename)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        file_handler = RotatingFileHandler(
            filename,
            maxBytes=1024 * 1024,
            backupCount=9
        )
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)

    logger.info('[Collector] Starting...')

    collector = BusDataCollector(config)

    # 设置SIGINT信号事件
    def signal_handler(signal, frame):
        logger.info('[Collector] Stopping...')
        collector.is_running = False
    signal.signal(signal.SIGINT, signal_handler)

    logger.info('[Collector] Started')

    collector.run()

    logger.info('[Collector] Exit')
