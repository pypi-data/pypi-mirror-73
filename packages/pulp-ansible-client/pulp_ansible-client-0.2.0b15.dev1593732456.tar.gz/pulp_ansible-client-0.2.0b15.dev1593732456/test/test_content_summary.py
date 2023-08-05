# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_ansible
from pulpcore.client.pulp_ansible.models.content_summary import ContentSummary  # noqa: E501
from pulpcore.client.pulp_ansible.rest import ApiException

class TestContentSummary(unittest.TestCase):
    """ContentSummary unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ContentSummary
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_ansible.models.content_summary.ContentSummary()  # noqa: E501
        if include_optional :
            return ContentSummary(
                added = {
                    'key' : {
                        'key' : '0'
                        }
                    }, 
                removed = {
                    'key' : {
                        'key' : '0'
                        }
                    }, 
                present = {
                    'key' : {
                        'key' : '0'
                        }
                    }
            )
        else :
            return ContentSummary(
                added = {
                    'key' : {
                        'key' : '0'
                        }
                    },
                removed = {
                    'key' : {
                        'key' : '0'
                        }
                    },
                present = {
                    'key' : {
                        'key' : '0'
                        }
                    },
        )

    def testContentSummary(self):
        """Test ContentSummary"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
