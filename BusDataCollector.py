#!/bin/python
# coding: utf8

import urllib2
import time
import json


def g_http_get(url):
    response = urllib2.urlopen(url)
    return response.read()


class BaseDataRequest:
    """数据请求基类"""

    baseUrl = 'http://www.zhbuswx.com/Handlers/BusQuery.ashx?handlerName=%(handler_name)s&_=%(timestamp)d'

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
        }
        external_param.update(self.__param)

        external_url = (self.baseUrl + '&' + self.__external_param) % external_param

        try:
            self.data = json.loads(g_http_get(external_url))
            self.data_fetched = True

            if type(self.data) is not dict:
                raise Exception("Unknown result %s" % self.data)

        except Exception as e:
            self.data = {}
            self.data_fetched = False
            print e.message


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
