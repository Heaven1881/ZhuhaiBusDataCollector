#!/bin/python
# coding: utf8

import unittest
import json

import BusDataCollector


class TestBusDataRequest(unittest.TestCase):

    def setUp(self):
        self.mock_exception = None
        self.mock_result = '{}'
        self.passed_args_url = ''
        self.mock_method_call_count = 0

        def mock_http_get(url):
            self.passed_args_url = url
            self.mock_method_call_count += 1
            if self.mock_exception:
                raise self.mock_exception
            return self.mock_result

        self.__http_get_backup = BusDataCollector.g_http_get
        BusDataCollector.g_http_get = mock_http_get

    def tearDown(self):
        BusDataCollector.g_http_get = self.__http_get_backup


class TestBusLineListRequest(TestBusDataRequest):

    def test_init(self):
        """测试初始化"""
        request = BusDataCollector.BusLineListRequest('A')

        self.assertFalse(request.data_fetched)
        self.assertFalse(any(request.data))
        self.assertEqual(self.mock_method_call_count, 0)

    def test_fetch_data(self):
        """测试基础功能"""
        self.mock_result = json.dumps({
            'key': 'value'
        })

        request = BusDataCollector.BusLineListRequest('3A')
        request.fetch_data()

        self.assertTrue('key=3A' in self.passed_args_url)
        self.assertTrue('handlerName=GetLineListByLineName' in self.passed_args_url)
        self.assertEqual(self.mock_method_call_count, 1)

        self.assertTrue('key' in request.data)
        self.assertTrue(request.data['key'] == 'value')

    def test_fetch_data_empty_result(self):
        """测试空返回值"""
        self.mock_result = ''

        request = BusDataCollector.BusLineListRequest('3A')
        request.fetch_data()

        self.assertFalse(request.data_fetched)
        self.assertFalse(any(request.data))

    def test_fetch_data_error_result(self):
        """测试返回值错误"""
        self.mock_result = '123456'

        request = BusDataCollector.BusLineListRequest('3A')
        request.fetch_data()

        self.assertFalse(request.data_fetched)
        self.assertFalse(any(request.data))

    def test_double_success_fetch_data(self):
        """如果请求已经成功，重复调用不会再次触发网络请求"""
        request = BusDataCollector.BusLineListRequest('3A')
        request.fetch_data()
        request.fetch_data()

        self.assertEqual(self.mock_method_call_count, 1)

    def test_double_fail_fetch_data(self):
        """失败的情况下可以重试"""
        self.mock_exception = Exception("Mock Exception")

        request = BusDataCollector.BusLineListRequest('3A')
        request.fetch_data()
        request.fetch_data()

        self.assertEqual(self.mock_method_call_count, 2)
