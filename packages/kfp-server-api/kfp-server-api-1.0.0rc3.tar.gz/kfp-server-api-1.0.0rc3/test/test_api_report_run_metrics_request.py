# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Kubeflow Pipelines API

    This file contains REST API specification for Kubeflow Pipelines. The file is autogenerated from the swagger definition.

    Contact: kubeflow-pipelines@google.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import kfp_server_api
from kfp_server_api.models.api_report_run_metrics_request import ApiReportRunMetricsRequest  # noqa: E501
from kfp_server_api.rest import ApiException

class TestApiReportRunMetricsRequest(unittest.TestCase):
    """ApiReportRunMetricsRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ApiReportRunMetricsRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kfp_server_api.models.api_report_run_metrics_request.ApiReportRunMetricsRequest()  # noqa: E501
        if include_optional :
            return ApiReportRunMetricsRequest(
                run_id = '0', 
                metrics = [
                    kfp_server_api.models.api_run_metric.apiRunMetric(
                        name = '0', 
                        node_id = '0', 
                        number_value = 1.337, 
                        format = 'UNSPECIFIED', )
                    ]
            )
        else :
            return ApiReportRunMetricsRequest(
        )

    def testApiReportRunMetricsRequest(self):
        """Test ApiReportRunMetricsRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
