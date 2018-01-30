#!/bin/python
# coding: utf8

import unittest

import BusDataRequest
import BusDataCollector


class MockMethod:

    def __init__(self, return_value=None):
        self.return_value = return_value
        self.__args_list = []
        self.call_count = 0

    def __call__(self, *args):
        self.__args_list.append(args)
        self.call_count += 1

        if type(self.return_value) is Exception:
            raise self.return_value
        return self.return_value

    def get_args(self, args_index=None, call_index=-1):
        if self.call_count < 1:
            return None

        if args_index is None:
            return self.__args_list[call_index]
        return self.__args_list[call_index][args_index]


class TestWithMock(unittest.TestCase):

    def setUp(self):
        # Mock网络访问函数
        self.mock_http_get = MockMethod('{}')
        self.__http_get_backup = BusDataRequest.g_http_get
        BusDataRequest.g_http_get = self.mock_http_get

        # Mock文件写入函数
        self.mock_append_one_line_to_file = MockMethod()
        self.__append_one_line_to_file_backup = BusDataCollector.g_append_one_line_to_file
        BusDataCollector.g_append_one_line_to_file = self.mock_append_one_line_to_file

    def tearDown(self):
        BusDataRequest.g_http_get = self.__http_get_backup
        BusDataCollector.g_append_one_line_to_file = self.__append_one_line_to_file_backup
