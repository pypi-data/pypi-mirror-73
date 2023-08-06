import logging
import uuid

import pytest

from tests.common import SdkIntegrationTestCase, eventually

logger = logging.getLogger(__name__)


@pytest.mark.integration
class SearchTestCase(SdkIntegrationTestCase):

    def entities_are_returned_in_search(self, search_func, expected_min_count):
        def search():
            result = search_func()
            self.assertTrue(len(result) >= expected_min_count)
            return result

        return eventually(search)

    def test_search_all_raises_error_for_invalid_count(self):
        self.assert_page_count_is_valid_for_paginated_resource_actions(lambda c: self.client.search(term='searchable', count=c))

    def test_search_packages_raises_error_for_invalid_count(self):
        self.assert_page_count_is_valid_for_paginated_resource_actions(lambda c: self.client.search_packages(term='searchable', count=c))

    def test_search_special_chars(self):
        payload = {
            "name": 'searchable package' + "_" + str(uuid.uuid4()),
            # hello chinese world
            "description":  "你好，世界",
            "publisher":  "datalake-mgmt",
            "manager_id":  "datalake-mgmt",
            "access_manager_id":  "datalake-mgmt",
            "tech_data_ops_id":  "datalake-mgmt",
            "topic":  "Academic/Education",
            "access":  'Restricted',
            "internal_data":  "No",
            "data_sensitivity":  "Public",
            "terms_and_conditions":  "Terms and Conditions"
        }
        self.client.register_package(**payload).package_id
        assert self.entities_are_returned_in_search(
            lambda: self.client.search_packages('你好'), 1
        )

    def test_search_packages(self):
        self.assertEqual(len(self.client.search_packages(term="")), 0)

        self.create_package("searchable package")
        search_term = "searchable"

        results = self.entities_are_returned_in_search(lambda: self.client.search_packages(search_term), 1)
        self.assertTrue(all([hasattr(package, "package_id") and search_term in package.name for package in results]))

    def test_search_datasets_raises_error_for_invalid_count(self):
        self.assert_page_count_is_valid_for_paginated_resource_actions(lambda c: self.client.search_datasets(term='searchable', count=c))

    def test_search_datasets(self):
        self.assertEqual(len(self.client.search_datasets(term="")), 0)

        package_id = self.create_package("package")
        builder = self.dataset_builder(package_id, "searchable dataset")
        builder = builder.with_external_storage(location="jdbc://somewhere")
        self.client.register_dataset(builder)

        search_term = "searchable"
        results = self.entities_are_returned_in_search(lambda: self.client.search_datasets(search_term), 1)
        for result in results:
            self.assertEqual(result.type, "dataset")
            self.assertIn(search_term, result.name)
