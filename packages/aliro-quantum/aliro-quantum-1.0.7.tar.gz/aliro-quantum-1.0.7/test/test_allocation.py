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
from openapi_client.models.allocation import Allocation  # noqa: E501
from openapi_client.rest import ApiException

class TestAllocation(unittest.TestCase):
    """Allocation unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Allocation
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = openapi_client.models.allocation.Allocation()  # noqa: E501
        if include_optional :
            return Allocation(
                allocated_qubits = [
                    56
                    ], 
                depth = 56, 
                program = '0', 
                num_gates_double = 56, 
                num_gates_single = 56, 
                num_measurements = 56, 
                num_swaps = 56
            )
        else :
            return Allocation(
        )

    def testAllocation(self):
        """Test Allocation"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
