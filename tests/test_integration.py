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

from datetime import date
from types import NoneType

import pytest

from ansys.grantami.system import ActivityLogFilter, ActivityLogItem, ActivityUsageMode

pytestmark = pytest.mark.integration(mi_versions=[(26, 1)])


def _validate_activity_log_item(item: ActivityLogItem, additional_checks: dict = None):
    """Validate an individual activity log item. By default, these checks are loose:

     * It is dynamic and is modified by all access to the system, so we cannot know before accessing it what will be
      included.
    * It is only updated at midnight each day, so we cannot make known changes and then check that those known changes
      have been made.
    """
    assert isinstance(item, ActivityLogItem)
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


def test_get_activity_log(connection):
    activity_log = connection.get_all_activity_items(page_size=None)
    item = next(activity_log)
    _validate_activity_log_item(item)
    item = next(activity_log)
    _validate_activity_log_item(item)


@pytest.mark.parametrize("page_size", [1, 2, 5, 10, 100])
def test_get_activity_log_paged(connection, page_size):
    activity_log = connection.get_all_activity_items(page_size=page_size)
    for _ in range(page_size):
        next(activity_log)
    item = next(activity_log)
    _validate_activity_log_item(item)


def test_get_activity_log_no_database(connection):
    no_database_filter = ActivityLogFilter().with_database_key(None)
    activity_log = connection.get_activity_items_where(no_database_filter)
    item = next(activity_log)
    _validate_activity_log_item(item, additional_checks={"database_key": None})


@pytest.mark.parametrize("usage_mode", [ActivityUsageMode.EDIT, ActivityUsageMode.VIEW])
def test_get_activity_log_by_usage_mode(connection, usage_mode):
    no_database_filter = ActivityLogFilter().with_usage_mode(usage_mode)
    activity_log = connection.get_activity_items_where(no_database_filter)
    item = next(activity_log)
    _validate_activity_log_item(item, additional_checks={"usage_mode": usage_mode})
