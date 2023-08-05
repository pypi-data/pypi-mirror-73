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
from openapi_client.models.job import Job  # noqa: E501
from openapi_client.rest import ApiException

class TestJob(unittest.TestCase):
    """Job unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Job
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = openapi_client.models.job.Job()  # noqa: E501
        if include_optional :
            return Job(
                allocations = openapi_client.models.job_allocations.Job_allocations(
                    allocated_circuits = [
                        openapi_client.models.allocation.Allocation(
                            allocated_qubits = [
                                56
                                ], 
                            depth = 56, 
                            program = '0', 
                            num_gates_double = 56, 
                            num_gates_single = 56, 
                            num_measurements = 56, 
                            num_swaps = 56, )
                        ], 
                    input_parameters = openapi_client.models.compilation_parameters.CompilationParameters(
                        compilation_type = '0', 
                        num_allocations = 56, ), 
                    language = '0', 
                    runtime = 1.337, ), 
                cancelling = True, 
                costs = openapi_client.models.job_costs.Job_costs(
                    reservation = 1.337, ), 
                errors = [
                    openapi_client.models.job_errors.Job_errors(
                        error_code = '0', 
                        error_message = '0', )
                    ], 
                execution = openapi_client.models.job_execution.Job_execution(
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
                            start_datetime = '0', ), ), ), 
                id = '0', 
                reservation = openapi_client.models.reservation.Reservation(
                    end_datetime = '0', 
                    id = '0', 
                    price = 1.337, 
                    start_datetime = '0', 
                    their_id = '0', ), 
                target = openapi_client.models.owner_details.OwnerDetails(
                    owners = {
                        'key' : openapi_client.models.owner_details_owners.OwnerDetails_owners(
                            devices = {
                                'key' : openapi_client.models.device_details.DeviceDetails(
                                    device_id = '0', 
                                    display_name = '0', 
                                    gates = [
                                        openapi_client.models.gate.Gate(
                                            fidelity = 1.337, 
                                            qubit_from = openapi_client.models.qubit.Qubit(
                                                fidelity_rotation = 1.337, 
                                                last_reported_fidelity_rotation_datetime = '0', 
                                                name = 56, 
                                                pos_x = 1.337, 
                                                pos_y = 1.337, 
                                                real_qubit = 56, ), 
                                            qubit_to = openapi_client.models.qubit.Qubit(
                                                fidelity_rotation = 1.337, 
                                                last_reported_fidelity_rotation_datetime = '0', 
                                                name = 56, 
                                                pos_x = 1.337, 
                                                pos_y = 1.337, 
                                                real_qubit = 56, ), 
                                            gate_type = '0', )
                                        ], 
                                    is_simulator = True, 
                                    last_calibration = '0', 
                                    max_shots = 56, 
                                    next_available_time = '0', 
                                    price = 1.337, 
                                    t1 = 1.337, 
                                    t2 = 1.337, )
                                }, )
                        }, )
            )
        else :
            return Job(
                allocations = openapi_client.models.job_allocations.Job_allocations(
                    allocated_circuits = [
                        openapi_client.models.allocation.Allocation(
                            allocated_qubits = [
                                56
                                ], 
                            depth = 56, 
                            program = '0', 
                            num_gates_double = 56, 
                            num_gates_single = 56, 
                            num_measurements = 56, 
                            num_swaps = 56, )
                        ], 
                    input_parameters = openapi_client.models.compilation_parameters.CompilationParameters(
                        compilation_type = '0', 
                        num_allocations = 56, ), 
                    language = '0', 
                    runtime = 1.337, ),
                execution = openapi_client.models.job_execution.Job_execution(
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
                            start_datetime = '0', ), ), ),
                target = openapi_client.models.owner_details.OwnerDetails(
                    owners = {
                        'key' : openapi_client.models.owner_details_owners.OwnerDetails_owners(
                            devices = {
                                'key' : openapi_client.models.device_details.DeviceDetails(
                                    device_id = '0', 
                                    display_name = '0', 
                                    gates = [
                                        openapi_client.models.gate.Gate(
                                            fidelity = 1.337, 
                                            qubit_from = openapi_client.models.qubit.Qubit(
                                                fidelity_rotation = 1.337, 
                                                last_reported_fidelity_rotation_datetime = '0', 
                                                name = 56, 
                                                pos_x = 1.337, 
                                                pos_y = 1.337, 
                                                real_qubit = 56, ), 
                                            qubit_to = openapi_client.models.qubit.Qubit(
                                                fidelity_rotation = 1.337, 
                                                last_reported_fidelity_rotation_datetime = '0', 
                                                name = 56, 
                                                pos_x = 1.337, 
                                                pos_y = 1.337, 
                                                real_qubit = 56, ), 
                                            gate_type = '0', )
                                        ], 
                                    is_simulator = True, 
                                    last_calibration = '0', 
                                    max_shots = 56, 
                                    next_available_time = '0', 
                                    price = 1.337, 
                                    t1 = 1.337, 
                                    t2 = 1.337, )
                                }, )
                        }, ),
        )

    def testJob(self):
        """Test Job"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
