# Copyright (C) 2025 ANSYS, Inc. and/or its affiliates.
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
import copy

import pytest

from ansys.grantami.serverapi_openapi.v2026r1.models import (
    GsaActivityLogCollectionMatchType,
    GsaActivityLogEntry,
    GsaActivityLogMatchType,
    GsaActivityLogUsageMode,
    GsaMiVersion,
)
from ansys.grantami.system._models import ActivityLogFilter, ActivityLogItem, ActivityUsageMode, GrantaMIVersion

from .activity_log_filter_parameters import get_parameters
from .common import APP_NAME_1, APP_NAME_2, DB_KEY, START_DATE, USERNAME, at_midnight


class TestActivityLogFilter:
    @staticmethod
    def _add_filter(filter_: ActivityLogFilter, filter_name: str, kwargs: dict) -> ActivityLogFilter:
        return getattr(filter_, filter_name)(**kwargs)

    @pytest.mark.parametrize(["inputs", "result_includes"], get_parameters())
    def test_filter_creation(self, inputs: dict, result_includes: dict):
        filter_ = ActivityLogFilter()
        for filter_name, filter_kwargs in inputs.items():
            if filter_kwargs is not None:
                self._add_filter(filter_, filter_name, filter_kwargs)

        result = filter_._to_model()

        for result_property_name, result_property in result_includes.items():
            assert getattr(result, result_property_name) == result_property

    def test_application_name_default_match_type(self):
        filter_ = ActivityLogFilter().with_application_name(APP_NAME_1)
        assert filter_._to_model().application_name_filter.match_type == GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE

    def test_application_names_default_match_type(self):
        filter_ = ActivityLogFilter().with_application_names([APP_NAME_1, APP_NAME_2])
        assert (
            filter_._to_model().application_names_collection_filter.collection_match_type
            == GsaActivityLogCollectionMatchType.COLLECTIONCONTAINS
        )

    def test_database_key_default_match_type(self):
        filter_ = ActivityLogFilter().with_database_key(DB_KEY)
        assert filter_._to_model().database_key_filter.match_type == GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE

    def test_date_from_default_inclusivity(self):
        filter_ = ActivityLogFilter().with_date_from(START_DATE)
        assert not filter_._to_model().date_filter.date_from_inclusive

    def test_date_to_default_inclusivity(self):
        filter_ = ActivityLogFilter().with_date_to(START_DATE)
        assert not filter_._to_model().date_filter.date_to_inclusive

    def test_username_filter_default_match_type(self):
        filter_ = ActivityLogFilter().with_username(USERNAME)
        assert filter_._to_model().username_filter.match_type == GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE

    def test_repr(self):
        assert repr(ActivityLogFilter()) == "<ActivityLogFilter ...>"


class TestActivityLogItem:
    item_without_db_key = ActivityLogItem(
        activity_date=START_DATE,
        application_names=[APP_NAME_1, APP_NAME_2],
        username=USERNAME,
        usage_mode=ActivityUsageMode.EDIT,
        database_key=None,
    )

    item_with_db_key = ActivityLogItem(
        activity_date=START_DATE,
        application_names=[APP_NAME_1, APP_NAME_2],
        username=USERNAME,
        usage_mode=ActivityUsageMode.EDIT,
        database_key=DB_KEY,
    )

    model_without_db_key = GsaActivityLogEntry(
        _date=at_midnight(START_DATE),
        application_names=[APP_NAME_1, APP_NAME_2],
        usage_mode=GsaActivityLogUsageMode.VIEW,
        username=USERNAME,
        database_key=None,
    )

    model_with_db_key = GsaActivityLogEntry(
        _date=at_midnight(START_DATE),
        application_names=[APP_NAME_1, APP_NAME_2],
        usage_mode=GsaActivityLogUsageMode.VIEW,
        username=USERNAME,
        database_key=DB_KEY,
    )

    model_with_single_app_name = GsaActivityLogEntry(
        _date=at_midnight(START_DATE),
        application_names=[APP_NAME_2],
        usage_mode=GsaActivityLogUsageMode.VIEW,
        username=USERNAME,
        database_key=DB_KEY,
    )

    def test_repr_with_db_key(self):
        expected_repr = (
            '<ActivityLogItem activity_date=2022-05-12, username="domain\\test_user", database_key="test_db_key", '
            "usage_mode=ActivityUsageMode.EDIT>"
        )
        assert repr(self.item_with_db_key) == expected_repr

    def test_repr_without_db_key(self):
        expected_repr = (
            '<ActivityLogItem activity_date=2022-05-12, username="domain\\test_user", database_key=None, '
            "usage_mode=ActivityUsageMode.EDIT>"
        )
        assert repr(self.item_without_db_key) == expected_repr

    def test_instantiate_from_model_with_db_key(self):
        item = ActivityLogItem._from_model(self.model_with_db_key)
        assert item.activity_date == START_DATE
        assert item.username == USERNAME
        assert item.database_key == DB_KEY
        assert item.usage_mode == ActivityUsageMode.VIEW
        assert item.activity_date == START_DATE
        assert set(item.application_names) == {APP_NAME_1, APP_NAME_2}

    def test_instantiate_from_model_without_db_key(self):
        item = ActivityLogItem._from_model(self.model_without_db_key)
        assert item.activity_date == START_DATE
        assert item.username == USERNAME
        assert item.database_key is None
        assert item.usage_mode == ActivityUsageMode.VIEW
        assert item.activity_date == START_DATE
        assert set(item.application_names) == {APP_NAME_1, APP_NAME_2}

    def test_instantiate_from_model_with_single_app_name(self):
        item = ActivityLogItem._from_model(self.model_with_single_app_name)
        assert item.activity_date == START_DATE
        assert item.username == USERNAME
        assert item.database_key == DB_KEY
        assert item.usage_mode == ActivityUsageMode.VIEW
        assert item.activity_date == START_DATE
        assert set(item.application_names) == {APP_NAME_2}


class TestVersion:
    version = GrantaMIVersion(
        major_minor_version=(28, 1),
        version=(28, 1, 19652, 353),
    )
    earlier_version = GrantaMIVersion(
        major_minor_version=(27, 2),
        version=(27, 2, 19653, 354),
    )

    def test_repr(self):
        assert repr(self.version) == "GrantaMIVersion(major_minor_version=(28, 1), version=(28, 1, 19652, 353))"

    def test_str(self):
        assert str(self.version) == "28.1.19652.353"

    def test_gt(self):
        assert self.version > self.earlier_version

    def test_gt_tuple(self):
        assert self.version > self.earlier_version.version

    def test_lt(self):
        assert self.earlier_version < self.version

    def test_lt_tuple(self):
        assert self.earlier_version.version < self.version

    def test_eq(self):
        assert self.version == copy.copy(self.version)

    def test_eq_tuple(self):
        assert self.version == self.version.version

    def test_neq(self):
        assert self.version != copy.copy(self.earlier_version)

    def test_neq_tuple(self):
        assert self.version != self.earlier_version.version

    def test_instantiate_from_model(self):
        model = GsaMiVersion(
            binary_compatibility_version="27.1.0.0",
            major_minor_version="27.1",
            version="27.1.123.456",
        )
        version = GrantaMIVersion._from_model(model)
        assert version.version == (27, 1, 123, 456)
        assert version.major_minor_version == (27, 1)
