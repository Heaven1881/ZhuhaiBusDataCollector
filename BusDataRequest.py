#!/bin/python
# coding: utf8

import urllib
import urllib2
import time
import json


def g_http_get(url):
    response = urllib2.urlopen(url)
    return response.read()


class BaseDataRequest:
    """数据请求基类"""

    baseUrl = 'http://www.zhbuswx.com/Handlers/BusQuery.ashx'

    def __init__(self, handler_name):
        self.__handler_name = handler_name
        self.__param = {}

        self.data_fetched = False
        self.data = {}
        self.last_exception = None

    def set_param(self, param):
        self.__param = param

    def fetch_data(self):
        if self.data_fetched:
            return

        external_param = {
            'handlerName': self.__handler_name,
            '_':  int(time.time() * 1000)
        }
        external_param.update(self.__param)

        external_url = self.baseUrl + '?' + urllib.urlencode(external_param)

        try:
            self.last_exception = None

            self.data = json.loads(g_http_get(external_url))
            self.data_fetched = True

            if type(self.data) is not dict:
                raise Exception("Unknown result %s" % self.data)

        except Exception as e:
            self.data = {}
            self.data_fetched = False
            self.last_exception = e


class BusLineListRequest(BaseDataRequest):
    """根据线路名称获取线路信息"""

    def __init__(self, key):
        BaseDataRequest.__init__(self, 'GetLineListByLineName')
        self.set_param({
            'key': key

        })


class BusStationListRequest(BaseDataRequest):
    """根据线路ID获取站点信息"""

    def __init__(self, line_id):
        BaseDataRequest.__init__(self, 'GetStationList')
        self.set_param({
            'lineId': line_id
        })


class BusInfoOnRoad(BaseDataRequest):
    """获取指定线路路上巴士的信息"""

    def __init__(self, line_name, from_station):
        BaseDataRequest.__init__(self, 'GetBusListOnRoad')
        self.set_param({
            'lineName': line_name,
            'fromStation': from_station
        })
