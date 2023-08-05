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
from openapi_client.models.submission_detail_response import SubmissionDetailResponse  # noqa: E501
from openapi_client.rest import ApiException

class TestSubmissionDetailResponse(unittest.TestCase):
    """SubmissionDetailResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SubmissionDetailResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = openapi_client.models.submission_detail_response.SubmissionDetailResponse()  # noqa: E501
        if include_optional :
            return SubmissionDetailResponse(
                submission_detail = {
  "circuits": [
    {
      "jobs": [
        {
          "allocations": {
            "inputParameters": {
              "compilationType": "fast",
              "numAllocations": 2
            }
          },
          "execution": {
            "parameters": {
              "numShots": 2,
              "timeout": 7.061401241503109
            }
          },
          "target": {
            "deviceName": "9q-square-qvm",
            "owner": "Rigetti"
          }
        }
      ],
      "language": "quil",
      "name": "quilTestCircuit",
      "body": "CNOT 0 1\nCNOT 0 1\nCNOT 1 0\nCNOT 1 2\nCNOT 2 3\nCNOT 4 3"
    }
  ],
  "createDate": "2020-03-03T15:01:57.687Z",
  "name": "quilTest"
}
, 
                submission_summary = openapi_client.models.submission_summary.SubmissionSummary(
                    completed_datetime = '0', 
                    jobs = openapi_client.models.submission_summary_jobs.SubmissionSummary_jobs(
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
                            ], ), 
                    name = '0', 
                    runtime = 1.337, 
                    submitted_datetime = '0', )
            )
        else :
            return SubmissionDetailResponse(
        )

    def testSubmissionDetailResponse(self):
        """Test SubmissionDetailResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
