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
import datetime

import honeywell
from honeywell.models.job_response import JobResponse  # noqa: E501
from honeywell.rest import ApiException

class TestJobResponse(unittest.TestCase):
    """JobResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test JobResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = honeywell.models.job_response.JobResponse()  # noqa: E501
        if include_optional :
            return JobResponse(
                job = '0', 
                status = '0'
            )
        else :
            return JobResponse(
        )

    def testJobResponse(self):
        """Test JobResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
