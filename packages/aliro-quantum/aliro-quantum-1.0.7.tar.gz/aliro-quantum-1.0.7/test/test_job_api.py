# coding: utf-8

"""
    Honeywell

    This is an api to connect to the Honeywell backend  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import honeywell
from honeywell.api.job_api import JobApi  # noqa: E501
from honeywell.rest import ApiException


class TestJobApi(unittest.TestCase):
    """JobApi unit test stubs"""

    def setUp(self):
        self.api = honeywell.api.job_api.JobApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_job_post(self):
        """Test case for job_post

        Quantum job may be submitted using the following API  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
