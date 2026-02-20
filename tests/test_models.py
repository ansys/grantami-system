# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0

import copy
from dataclasses import asdict

import pytest

from ansys.grantami.serverapi_openapi.v2026r1.models import (
    GsaActivityLogCollectionMatchType,
    GsaActivityLogEntry,
    GsaActivityLogMatchType,
    GsaActivityLogUsageMode,
    GsaMiVersion,
)
from ansys.grantami.system._models import ActivityItem, ActivityReportFilter, ActivityUsageMode, GrantaMIVersion

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
            "ActivityItem(activity_date=datetime.date(2022, 5, 12), application_names=['test_app_name', "
            r"'app_name_with 😂'], username='domain\\test_user', usage_mode=<ActivityUsageMode.EDIT: 'edit'>, "
            "database_key='test_db_key')"
        )
        assert repr(self.item_with_db_key) == expected_repr

    def test_repr_without_db_key(self):
        expected_repr = (
            "ActivityItem(activity_date=datetime.date(2022, 5, 12), application_names=['test_app_name', "
            r"'app_name_with 😂'], username='domain\\test_user', usage_mode=<ActivityUsageMode.EDIT: 'edit'>, "
            "database_key=None)"
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

    def test_model_to_dict_with_db_key(self):
        dict_representation = asdict(self.item_with_db_key)
        assert dict_representation == dict(
            activity_date=START_DATE,
            application_names=[APP_NAME_1, APP_NAME_2],
            username=USERNAME,
            usage_mode=ActivityUsageMode.EDIT,
            database_key=DB_KEY,
        )

    def test_model_to_dict_without_db_key(self):
        dict_representation = asdict(self.item_without_db_key)
        assert dict_representation == dict(
            activity_date=START_DATE,
            application_names=[APP_NAME_1, APP_NAME_2],
            username=USERNAME,
            usage_mode=ActivityUsageMode.EDIT,
            database_key=None,
        )


class TestVersion:
    version = GrantaMIVersion(
        version=(28, 1, 19652, 353),
        binary_compatibility_version="28.1.0.0",
    )
    compatible_version = GrantaMIVersion(
        version=(28, 1, 19652, 378),
        binary_compatibility_version="28.1.0.0",
    )
    valid_model = GsaMiVersion(version="27.1.123.456", binary_compatibility_version="27.1.0.0")
    valid_model_long = GsaMiVersion(
        version="24.2.123.456.789.1.2.3.5.7.6.1",
        binary_compatibility_version="24.2.123.456.0.0.0.0.0.0.0.0",
    )
    invalid_model_comma_separated = GsaMiVersion(version="25,8", binary_compatibility_version="25,8,0,0")
    invalid_model_empty_string = GsaMiVersion(version="", binary_compatibility_version="")

    def test_repr(self):
        expected_repr = "GrantaMIVersion(version=(28, 1, 19652, 353), binary_compatibility_version='28.1.0.0')"
        assert repr(self.version) == expected_repr

    def test_str(self):
        assert str(self.version) == "28.1.19652.353"

    def test_eq(self):
        assert self.version == copy.copy(self.version)

    def test_neq(self):
        assert self.version != copy.copy(self.compatible_version)

    def test_compatible(self):
        assert self.version.binary_compatibility_version == self.compatible_version.binary_compatibility_version

    def test_instantiate_from_model(self):
        version = GrantaMIVersion._from_model(self.valid_model)
        assert version.version == (27, 1, 123, 456)
        assert version.major_minor_version == (27, 1)
        assert version.binary_compatibility_version == "27.1.0.0"

    def test_instantiate_from_model_long(self):
        version = GrantaMIVersion._from_model(self.valid_model_long)
        assert version.version == (24, 2, 123, 456, 789, 1, 2, 3, 5, 7, 6, 1)
        assert version.major_minor_version == (24, 2)
        assert version.binary_compatibility_version == "24.2.123.456.0.0.0.0.0.0.0.0"

    def test_instantiate_from_invalid_model_raises_value_error(self):
        with pytest.raises(ValueError, match="'25,8' is not a valid version string"):
            GrantaMIVersion._from_model(self.invalid_model_comma_separated)

    def test_instantiate_from_empty_string_model_raises_value_error(self):
        with pytest.raises(ValueError, match="'' is not a valid version string"):
            GrantaMIVersion._from_model(self.invalid_model_empty_string)
