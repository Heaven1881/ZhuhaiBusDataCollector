#!/bin/python
# coding: utf8

import urllib2
import time
import json


class BaseDataRequest:
    """数据请求基类"""

    base_url = 'http://www.zhbuswx.com/Handlers/BusQuery.ashx?handlerName=%(handler_name)s&_=%(timestamp)d'

    def __init__(self, external_param, handler_name):
        self.__external_param = external_param
        self.__handler_name = handler_name
        self.__param = {}

        self.data_fetched = False
        self.data = {}

    def set_param(self, param):
        self.__param = param

    def fetch_data(self):
        if self.data_fetched:
            return

        external_param = {
            'handler_name': self.__handler_name,
            'timestamp': time.time() * 1000
        }.update(self.__param)
        external_url = self.base_url + '&' + self.__external_param % external_param

        response = urllib2.urlopen(external_url)

        self.data = json.loads(response.read())
        self.data_fetched = True


class BusLineListRequest(BaseDataRequest):
    """根据线路名称获取线路信息"""

    def __init__(self, key):
        BaseDataRequest.__init__(
            self,
            'key=%(key)s',
            'GetLineListByLineName'
        )
        self.set_param({
            'key': key

        })


class BusStationListRequest(BaseDataRequest):
    """根据线路ID获取站点信息"""

    def __init__(self, line_id):
        BaseDataRequest.__init__(
            self,
            'lineId=%(line_id)s',
            'GetStationList'
        )
        self.set_param({
            'line_id': line_id
        })
