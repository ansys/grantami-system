# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0

from datetime import date
from types import NoneType

import pytest

from ansys.grantami.system import ActivityItem, ActivityReportFilter, ActivityUsageMode

pytestmark = pytest.mark.integration(mi_versions=[(26, 1)])


def _validate_activity_log_item(item: ActivityItem, additional_checks: dict = None):
    """Validate an individual activity log item. By default, these checks are loose:

     * It is dynamic and is modified by all access to the system, so we cannot know before accessing it what will be
      included.
    * It is only updated at midnight each day, so we cannot make known changes and then check that those known changes
      have been made.
    """
    assert isinstance(item, ActivityItem)
    assert item.activity_date < date.today()  # Logs only include entries from the previous day
    assert isinstance(item.application_names, list)
    assert all(isinstance(app_name, str) for app_name in item.application_names)
    assert isinstance(item.database_key, (str, NoneType))
    assert isinstance(item.usage_mode, ActivityUsageMode)
    assert isinstance(item.username, str)
    if additional_checks is None:
        return
    for attr_name, value in additional_checks.items():
        assert getattr(item, attr_name) == value


@pytest.mark.parametrize("page_size", [1, 2, 5, 10, 100])
def test_get_activity_log_paged(connection_sysadmin, page_size):
    activity_log = connection_sysadmin.get_activity_report(page_size=page_size)
    for _ in range(page_size):
        next(activity_log)
    item = next(activity_log)
    _validate_activity_log_item(item)


def test_get_activity_log_no_database(connection_sysadmin):
    no_database_filter = ActivityReportFilter().with_database_key(None)
    activity_log = connection_sysadmin.get_activity_report_where(no_database_filter)
    item = next(activity_log)
    _validate_activity_log_item(item, additional_checks={"database_key": None})


@pytest.mark.parametrize("usage_mode", [ActivityUsageMode.EDIT, ActivityUsageMode.VIEW])
def test_get_activity_log_by_usage_mode(connection_sysadmin, usage_mode):
    usage_mode_filter = ActivityReportFilter().with_usage_mode(usage_mode)
    activity_log = connection_sysadmin.get_activity_report_where(usage_mode_filter)
    item = next(activity_log)
    _validate_activity_log_item(item, additional_checks={"usage_mode": usage_mode})


def test_get_server_version(connection_sysadmin):
    version = connection_sysadmin.get_granta_mi_version()
    assert version.major_minor_version
    assert version.version
    assert version.binary_compatibility_version
