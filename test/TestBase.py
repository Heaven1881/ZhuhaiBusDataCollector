#!/bin/python
# coding: utf8

import unittest
import BusDataRequest


class TestWithNetworkMock(unittest.TestCase):

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

        self.__http_get_backup = BusDataRequest.g_http_get
        BusDataRequest.g_http_get = mock_http_get

    def tearDown(self):
        BusDataRequest.g_http_get = self.__http_get_backup
