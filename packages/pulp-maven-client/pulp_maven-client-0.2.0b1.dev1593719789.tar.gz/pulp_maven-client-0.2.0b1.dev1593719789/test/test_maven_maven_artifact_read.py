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

import pulpcore.client.pulp_maven
from pulpcore.client.pulp_maven.models.maven_maven_artifact_read import MavenMavenArtifactRead  # noqa: E501
from pulpcore.client.pulp_maven.rest import ApiException

class TestMavenMavenArtifactRead(unittest.TestCase):
    """MavenMavenArtifactRead unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MavenMavenArtifactRead
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_maven.models.maven_maven_artifact_read.MavenMavenArtifactRead()  # noqa: E501
        if include_optional :
            return MavenMavenArtifactRead(
                pulp_href = '0', 
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                artifact = '0', 
                group_id = '0', 
                artifact_id = '0', 
                version = '0', 
                filename = '0'
            )
        else :
            return MavenMavenArtifactRead(
                artifact = '0',
        )

    def testMavenMavenArtifactRead(self):
        """Test MavenMavenArtifactRead"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
