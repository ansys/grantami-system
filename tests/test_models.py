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
import pytest

from ansys.grantami.serverapi_openapi.v2026r1.models import (
    GsaActivityLogCollectionMatchType,
    GsaActivityLogEntry,
    GsaActivityLogMatchType,
    GsaActivityLogUsageMode,
)
from ansys.grantami.system._models import ActivityItem, ActivityReportFilter, ActivityUsageMode

from .activity_log_filter_parameters import get_parameters
from .common import APP_NAME_1, APP_NAME_2, DB_KEY, START_DATE, USERNAME, at_midnight


class TestActivityLogFilter:
    @staticmethod
    def _add_filter(filter_: ActivityReportFilter, filter_name: str, kwargs: dict) -> ActivityReportFilter:
        return getattr(filter_, filter_name)(**kwargs)

    @pytest.mark.parametrize(["inputs", "result_includes"], get_parameters())
    def test_filter_creation(self, inputs: dict, result_includes: dict):
        filter_ = ActivityReportFilter()
        for filter_name, filter_kwargs in inputs.items():
            if filter_kwargs is not None:
                self._add_filter(filter_, filter_name, filter_kwargs)

        result = filter_._to_model()

        for result_property_name, result_property in result_includes.items():
            assert getattr(result, result_property_name) == result_property

    def test_application_name_default_match_type(self):
        filter_ = ActivityReportFilter().with_application_name(APP_NAME_1)
        assert filter_._to_model().application_name_filter.match_type == GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE

    def test_application_names_default_match_type(self):
        filter_ = ActivityReportFilter().with_application_names([APP_NAME_1, APP_NAME_2])
        assert (
            filter_._to_model().application_names_collection_filter.collection_match_type
            == GsaActivityLogCollectionMatchType.COLLECTIONCONTAINS
        )

    def test_database_key_default_match_type(self):
        filter_ = ActivityReportFilter().with_database_key(DB_KEY)
        assert filter_._to_model().database_key_filter.match_type == GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE

    def test_date_from_default_inclusivity(self):
        filter_ = ActivityReportFilter().with_date_from(START_DATE)
        assert not filter_._to_model().date_filter.date_from_inclusive

    def test_date_to_default_inclusivity(self):
        filter_ = ActivityReportFilter().with_date_to(START_DATE)
        assert not filter_._to_model().date_filter.date_to_inclusive

    def test_username_filter_default_match_type(self):
        filter_ = ActivityReportFilter().with_username(USERNAME)
        assert filter_._to_model().username_filter.match_type == GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE

    def test_repr(self):
        assert repr(ActivityReportFilter()) == "<ActivityReportFilter ...>"


class TestActivityLogItem:
    item_without_db_key = ActivityItem(
        activity_date=START_DATE,
        application_names=[APP_NAME_1, APP_NAME_2],
        username=USERNAME,
        usage_mode=ActivityUsageMode.EDIT,
        database_key=None,
    )

    item_with_db_key = ActivityItem(
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
            '<ActivityItem activity_date=2022-05-12, username="domain\\test_user", database_key="test_db_key", '
            "usage_mode=ActivityUsageMode.EDIT>"
        )
        assert repr(self.item_with_db_key) == expected_repr

    def test_repr_without_db_key(self):
        expected_repr = (
            '<ActivityItem activity_date=2022-05-12, username="domain\\test_user", database_key=None, '
            "usage_mode=ActivityUsageMode.EDIT>"
        )
        assert repr(self.item_without_db_key) == expected_repr

    def test_instantiate_from_model_with_db_key(self):
        item = ActivityItem._from_model(self.model_with_db_key)
        assert item.activity_date == START_DATE
        assert item.username == USERNAME
        assert item.database_key == DB_KEY
        assert item.usage_mode == ActivityUsageMode.VIEW
        assert item.activity_date == START_DATE
        assert set(item.application_names) == {APP_NAME_1, APP_NAME_2}

    def test_instantiate_from_model_without_db_key(self):
        item = ActivityItem._from_model(self.model_without_db_key)
        assert item.activity_date == START_DATE
        assert item.username == USERNAME
        assert item.database_key is None
        assert item.usage_mode == ActivityUsageMode.VIEW
        assert item.activity_date == START_DATE
        assert set(item.application_names) == {APP_NAME_1, APP_NAME_2}

    def test_instantiate_from_model_with_single_app_name(self):
        item = ActivityItem._from_model(self.model_with_single_app_name)
        assert item.activity_date == START_DATE
        assert item.username == USERNAME
        assert item.database_key == DB_KEY
        assert item.usage_mode == ActivityUsageMode.VIEW
        assert item.activity_date == START_DATE
        assert set(item.application_names) == {APP_NAME_2}
