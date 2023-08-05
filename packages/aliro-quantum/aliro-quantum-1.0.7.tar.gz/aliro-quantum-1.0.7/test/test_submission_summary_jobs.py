# coding: utf-8

"""
    Aliro Quantum App

    This is an api for the Aliro Quantum App  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import openapi_client
from openapi_client.models.submission_summary_jobs import SubmissionSummaryJobs  # noqa: E501
from openapi_client.rest import ApiException

class TestSubmissionSummaryJobs(unittest.TestCase):
    """SubmissionSummaryJobs unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SubmissionSummaryJobs
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = openapi_client.models.submission_summary_jobs.SubmissionSummaryJobs()  # noqa: E501
        if include_optional :
            return SubmissionSummaryJobs(
                cancelled = [
                    '0'
                    ], 
                completed = [
                    '0'
                    ], 
                error = [
                    '0'
                    ], 
                initiated = [
                    '0'
                    ], 
                in_progress = [
                    '0'
                    ]
            )
        else :
            return SubmissionSummaryJobs(
        )

    def testSubmissionSummaryJobs(self):
        """Test SubmissionSummaryJobs"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
