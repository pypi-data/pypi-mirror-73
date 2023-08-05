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

import pulpcore.client.pulp_2to3_migration
from pulpcore.client.pulp_2to3_migration.models.pulp2to3_migration_pulp2_repository_read import Pulp2to3MigrationPulp2RepositoryRead  # noqa: E501
from pulpcore.client.pulp_2to3_migration.rest import ApiException

class TestPulp2to3MigrationPulp2RepositoryRead(unittest.TestCase):
    """Pulp2to3MigrationPulp2RepositoryRead unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Pulp2to3MigrationPulp2RepositoryRead
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_2to3_migration.models.pulp2to3_migration_pulp2_repository_read.Pulp2to3MigrationPulp2RepositoryRead()  # noqa: E501
        if include_optional :
            return Pulp2to3MigrationPulp2RepositoryRead(
                pulp_href = '0', 
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                pulp2_object_id = '0', 
                pulp2_repo_id = '0', 
                pulp2_repo_type = '0', 
                is_migrated = True, 
                not_in_plan = True, 
                pulp3_repository_version = '0', 
                pulp3_remote_href = '0', 
                pulp3_publication_href = '0', 
                pulp3_distribution_hrefs = [
                    '0'
                    ], 
                pulp3_repository_href = '0'
            )
        else :
            return Pulp2to3MigrationPulp2RepositoryRead(
                pulp2_object_id = '0',
                pulp2_repo_id = '0',
                pulp2_repo_type = '0',
        )

    def testPulp2to3MigrationPulp2RepositoryRead(self):
        """Test Pulp2to3MigrationPulp2RepositoryRead"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
