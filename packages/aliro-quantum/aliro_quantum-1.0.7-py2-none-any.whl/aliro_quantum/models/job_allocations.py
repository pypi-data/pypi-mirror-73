# coding: utf-8

"""
    Aliro Quantum App

    This is an api for the Aliro Quantum App  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from aliro_quantum.configuration import Configuration


class JobAllocations(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'allocated_circuits': 'list[Allocation]',
        'input_parameters': 'CompilationParameters',
        'language': 'str',
        'runtime': 'float'
    }

    attribute_map = {
        'allocated_circuits': 'allocatedCircuits',
        'input_parameters': 'inputParameters',
        'language': 'language',
        'runtime': 'runtime'
    }

    def __init__(self, allocated_circuits=None, input_parameters=None, language=None, runtime=None, local_vars_configuration=None):  # noqa: E501
        """JobAllocations - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._allocated_circuits = None
        self._input_parameters = None
        self._language = None
        self._runtime = None
        self.discriminator = None

        if allocated_circuits is not None:
            self.allocated_circuits = allocated_circuits
        self.input_parameters = input_parameters
        if language is not None:
            self.language = language
        if runtime is not None:
            self.runtime = runtime

    @property
    def allocated_circuits(self):
        """Gets the allocated_circuits of this JobAllocations.  # noqa: E501


        :return: The allocated_circuits of this JobAllocations.  # noqa: E501
        :rtype: list[Allocation]
        """
        return self._allocated_circuits

    @allocated_circuits.setter
    def allocated_circuits(self, allocated_circuits):
        """Sets the allocated_circuits of this JobAllocations.


        :param allocated_circuits: The allocated_circuits of this JobAllocations.  # noqa: E501
        :type: list[Allocation]
        """

        self._allocated_circuits = allocated_circuits

    @property
    def input_parameters(self):
        """Gets the input_parameters of this JobAllocations.  # noqa: E501


        :return: The input_parameters of this JobAllocations.  # noqa: E501
        :rtype: CompilationParameters
        """
        return self._input_parameters

    @input_parameters.setter
    def input_parameters(self, input_parameters):
        """Sets the input_parameters of this JobAllocations.


        :param input_parameters: The input_parameters of this JobAllocations.  # noqa: E501
        :type: CompilationParameters
        """
        if self.local_vars_configuration.client_side_validation and input_parameters is None:  # noqa: E501
            raise ValueError("Invalid value for `input_parameters`, must not be `None`")  # noqa: E501

        self._input_parameters = input_parameters

    @property
    def language(self):
        """Gets the language of this JobAllocations.  # noqa: E501


        :return: The language of this JobAllocations.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this JobAllocations.


        :param language: The language of this JobAllocations.  # noqa: E501
        :type: str
        """

        self._language = language

    @property
    def runtime(self):
        """Gets the runtime of this JobAllocations.  # noqa: E501

        the runtume of the optimizatin compilation in milliseconds  # noqa: E501

        :return: The runtime of this JobAllocations.  # noqa: E501
        :rtype: float
        """
        return self._runtime

    @runtime.setter
    def runtime(self, runtime):
        """Sets the runtime of this JobAllocations.

        the runtume of the optimizatin compilation in milliseconds  # noqa: E501

        :param runtime: The runtime of this JobAllocations.  # noqa: E501
        :type: float
        """

        self._runtime = runtime

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, JobAllocations):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, JobAllocations):
            return True

        return self.to_dict() != other.to_dict()
