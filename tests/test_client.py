# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from unittest.mock import Mock

import pytest

from ansys.grantami.serverapi_openapi.v2026r1 import models
from ansys.grantami.serverapi_openapi.v2026r1.api import ActivityLogApi, SchemaApi
from ansys.grantami.serverapi_openapi.v2026r1.models import (
    GsaActivityLogEntriesFilter,
    GsaActivityLogEntriesInfo,
    GsaActivityLogEntry,
    GsaActivityLogUsageMode,
    GsaMiVersion,
)
from ansys.grantami.system import ActivityReportFilter
from ansys.grantami.system._connection import (
    PROXY_PATH,
    SystemApiClient,
)


@pytest.fixture
def client(request):
    client = SystemApiClient(
        session=Mock(),
        service_layer_url="http://server_name/mi_servicelayer",
        configuration=Mock(),
    )
    client.setup_client(models)
    return client


def test_client_has_expected_api_url(client):
    assert client.api_url == "http://server_name/mi_servicelayer" + PROXY_PATH


def test_client_repr(client):
    assert repr(client) == "<SystemApiClient url: http://server_name/mi_servicelayer>"


class TestActivityLog:
    @pytest.fixture
    def items(self):
        return [
            GsaActivityLogEntry(
                _date=datetime.now(),
                application_names=["App"],
                usage_mode=GsaActivityLogUsageMode.VIEW,
                username="Test",
                database_key=None,
            ),
            GsaActivityLogEntry(
                _date=datetime.now(),
                application_names=["App2"],
                usage_mode=GsaActivityLogUsageMode.EDIT,
                username="Test2",
                database_key="test",
            ),
            GsaActivityLogEntry(
                _date=datetime.now(),
                application_names=["App3", "Application 3"],
                usage_mode=GsaActivityLogUsageMode.EDIT,
                username="Test3",
                database_key="test3",
            ),
        ]

    @pytest.fixture
    def filter_(self):
        return ActivityReportFilter().with_database_key(database_key=None).with_username("user_name")

    @pytest.fixture
    def api_method(self, monkeypatch, items):
        next_index = 0

        def side_effect(page_size=1000, **kwargs):
            return_value = Mock(spec=GsaActivityLogEntriesInfo)
            if page_size is None:
                return return_value.items
            nonlocal next_index
            return_value.entries = items[next_index : next_index + page_size]
            next_index = next_index + page_size
            return return_value

        mocked_method = Mock(side_effect=side_effect)
        monkeypatch.setattr(ActivityLogApi, "get_entries", mocked_method)
        return mocked_method

    @pytest.mark.parametrize("page_size", [4, 5, 50000])
    def test_read_all_items_page_size_larger_than_response_length(self, client, api_method, page_size):
        item_iterator = client.get_activity_report(page_size=page_size)
        api_method.assert_not_called()

        items = list(item_iterator)
        assert api_method.call_count == 2
        common_called_kwargs = {
            "body": GsaActivityLogEntriesFilter(),
            "page_size": page_size,
        }
        assert api_method.call_args_list[0].kwargs == dict(page=1, **common_called_kwargs)
        assert api_method.call_args_list[1].kwargs == dict(page=2, **common_called_kwargs)
        assert len(list(items)) == 3

    def test_read_all_items_page_size_equal_to_response_length(self, client, api_method):
        item_iterator = client.get_activity_report(page_size=3)
        api_method.assert_not_called()

        items = list(item_iterator)
        assert api_method.call_count == 2
        common_called_kwargs = {
            "body": GsaActivityLogEntriesFilter(),
            "page_size": 3,
        }
        assert api_method.call_args_list[0].kwargs == dict(page=1, **common_called_kwargs)
        assert api_method.call_args_list[1].kwargs == dict(page=2, **common_called_kwargs)
        assert len(list(items)) == 3

    def test_read_all_items_page_size_1(self, client, api_method):
        item_iterator = client.get_activity_report(page_size=1)
        api_method.assert_not_called()

        items = list(item_iterator)
        assert api_method.call_count == 4
        common_called_kwargs = {
            "body": GsaActivityLogEntriesFilter(),
            "page_size": 1,
        }
        assert api_method.call_args_list[0].kwargs == dict(page=1, **common_called_kwargs)
        assert api_method.call_args_list[1].kwargs == dict(page=2, **common_called_kwargs)
        assert api_method.call_args_list[2].kwargs == dict(page=3, **common_called_kwargs)
        assert api_method.call_args_list[3].kwargs == dict(page=4, **common_called_kwargs)
        assert len(list(items)) == 3

    def test_read_all_items_page_size_2(self, client, api_method):
        item_iterator = client.get_activity_report(page_size=2)
        api_method.assert_not_called()

        items = list(item_iterator)
        assert api_method.call_count == 3
        common_called_kwargs = {
            "body": GsaActivityLogEntriesFilter(),
            "page_size": 2,
        }
        assert api_method.call_args_list[0].kwargs == dict(page=1, **common_called_kwargs)
        assert api_method.call_args_list[1].kwargs == dict(page=2, **common_called_kwargs)
        assert api_method.call_args_list[2].kwargs == dict(page=3, **common_called_kwargs)
        assert len(list(items)) == 3

    def test_with_filter_paged(self, client, api_method, filter_):
        item_iterator = client.get_activity_report_where(filter_, page_size=1)
        api_method.assert_not_called()

        items = list(item_iterator)
        assert api_method.call_count == 4
        common_called_kwargs = {
            "body": filter_._to_model(),
            "page_size": 1,
        }
        assert api_method.call_args_list[0].kwargs == dict(page=1, **common_called_kwargs)
        assert api_method.call_args_list[1].kwargs == dict(page=2, **common_called_kwargs)
        assert api_method.call_args_list[2].kwargs == dict(page=3, **common_called_kwargs)
        assert api_method.call_args_list[3].kwargs == dict(page=4, **common_called_kwargs)
        assert len(list(items)) == 3


class TestGrantaMIVersion:
    binary_compatibility_version = "1.2.0.0"
    major_minor_version = "1.2"
    version = "1.2.3.4"
    version_tuple = (1, 2, 3, 4)

    @pytest.fixture
    def api_method(self, monkeypatch):
        return_value = GsaMiVersion(
            binary_compatibility_version=self.binary_compatibility_version,
            major_minor_version=self.major_minor_version,
            version=self.version,
        )
        mocked_method = Mock(return_value=return_value)
        monkeypatch.setattr(SchemaApi, "get_version", mocked_method)
        return mocked_method

    def test_get_version_number(self, client, api_method):
        version = client.get_granta_mi_version()
        api_method.assert_called_once_with()
        assert version.major_minor_version == self.version_tuple[0:2]
        assert version.version == self.version_tuple
