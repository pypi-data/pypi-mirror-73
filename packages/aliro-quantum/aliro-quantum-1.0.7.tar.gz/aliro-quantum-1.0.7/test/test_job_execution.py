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
from openapi_client.models.job_execution import JobExecution  # noqa: E501
from openapi_client.rest import ApiException

class TestJobExecution(unittest.TestCase):
    """JobExecution unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test JobExecution
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = openapi_client.models.job_execution.JobExecution()  # noqa: E501
        if include_optional :
            return JobExecution(
                parameters = openapi_client.models.execution_parameters.ExecutionParameters(
                    num_shots = 56, 
                    output_type = '0', ), 
                results = openapi_client.models.execution_results.ExecutionResults(
                    real = openapi_client.models.results_data.ResultsData(
                        empirical_sso = 1.337, 
                        end_datetime = '0', 
                        measurements = openapi_client.models.results_data_measurements.ResultsData_measurements(
                            raw = [
                                [
                                    [
                                        56
                                        ]
                                    ]
                                ], 
                            weighted_combination = {
                                'key' : 1.337
                                }, ), 
                        runtime = 1.337, 
                        start_datetime = '0', ), 
                    simulated = openapi_client.models.results_data.ResultsData(
                        empirical_sso = 1.337, 
                        end_datetime = '0', 
                        runtime = 1.337, 
                        start_datetime = '0', ), )
            )
        else :
            return JobExecution(
                parameters = openapi_client.models.execution_parameters.ExecutionParameters(
                    num_shots = 56, 
                    output_type = '0', ),
        )

    def testJobExecution(self):
        """Test JobExecution"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
