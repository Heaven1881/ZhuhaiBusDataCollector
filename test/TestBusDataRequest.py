#!/bin/python
# coding: utf8

import json

import BusDataRequest
from test.TestBase import TestWithNetworkMock


class TestBusLineListRequest(TestWithNetworkMock):

    def test_init(self):
        """测试初始化"""
        request = BusDataRequest.BusLineListRequest('A')

        self.assertFalse(request.data_fetched)
        self.assertFalse(any(request.data))
        self.assertEqual(self.mock_method_call_count, 0)

    def test_fetch_data(self):
        """测试基础功能"""
        self.mock_result = json.dumps({
            'key': 'value'
        })

        request = BusDataRequest.BusLineListRequest('3A')
        request.fetch_data()

        self.assertTrue('key=3A' in self.passed_args_url)
        self.assertTrue('handlerName=GetLineListByLineName' in self.passed_args_url)
        self.assertEqual(self.mock_method_call_count, 1)

        self.assertTrue('key' in request.data)
        self.assertTrue(request.data['key'] == 'value')

    def test_fetch_data_empty_result(self):
        """测试空返回值"""
        self.mock_result = ''

        request = BusDataRequest.BusLineListRequest('3A')
        request.fetch_data()

        self.assertFalse(request.data_fetched)
        self.assertFalse(any(request.data))

    def test_fetch_data_error_result(self):
        """测试返回值错误"""
        self.mock_result = '123456'

        request = BusDataRequest.BusLineListRequest('3A')
        request.fetch_data()

        self.assertFalse(request.data_fetched)
        self.assertFalse(any(request.data))

    def test_double_success_fetch_data(self):
        """如果请求已经成功，重复调用不会再次触发网络请求"""
        request = BusDataRequest.BusLineListRequest('3A')
        request.fetch_data()
        request.fetch_data()

        self.assertEqual(self.mock_method_call_count, 1)

    def test_double_fail_fetch_data(self):
        """失败的情况下可以重试"""
        self.mock_exception = Exception("Mock Exception")

        request = BusDataRequest.BusLineListRequest('3A')
        request.fetch_data()
        request.fetch_data()

        self.assertEqual(self.mock_method_call_count, 2)


class TestBusInfoOnRoadRequest(TestWithNetworkMock):

    def test_fetch_data(self):
        """测试基础功能"""
        self.mock_result = json.dumps({
            'key': 'value'
        })

        request = BusDataRequest.BusInfoOnRoad('3A', '九洲港')
        request.fetch_data()

        self.assertTrue('lineName=3A' in self.passed_args_url)
        self.assertTrue('fromStation=%E4%B9%9D%E6%B4%B2%E6%B8%AF' in self.passed_args_url)
        self.assertTrue('handlerName=GetBusListOnRoad' in self.passed_args_url)
        self.assertEqual(self.mock_method_call_count, 1)

        self.assertTrue('key' in request.data)
        self.assertTrue(request.data['key'] == 'value')
