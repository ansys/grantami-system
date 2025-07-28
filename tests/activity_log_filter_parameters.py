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

import itertools

from ansys.openapi.common import Unset
import pytest

from ansys.grantami.serverapi_openapi.v2026r1.models import (
    GsaActivityLogApplicationNameFilter,
    GsaActivityLogApplicationNamesCollectionFilter,
    GsaActivityLogCollectionMatchType,
    GsaActivityLogDatabaseKeyFilter,
    GsaActivityLogDateFilter,
    GsaActivityLogMatchType,
    GsaActivityLogUsageMode,
    GsaActivityLogUsageModeFilter,
    GsaActivityLogUsernameFilter,
)
from ansys.grantami.system._models import ActivityUsageMode

from .common import APP_NAME_1, APP_NAME_2, DB_KEY, END_DATE, START_DATE, USERNAME, at_midnight

application_name = [
    {
        "with_application_name": None,
        "result_includes": {"application_name_filter": Unset},
        "label": "no app name filter",
    },
    {
        "with_application_name": {
            "application_name": APP_NAME_1,
            "exact_match": False,
        },
        "result_includes": {
            "application_name_filter": GsaActivityLogApplicationNameFilter(
                application_name_to_match=APP_NAME_1,
                match_type=GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE,
            )
        },
        "label": "non-exact app name",
    },
    {
        "with_application_name": {
            "application_name": APP_NAME_2,
            "exact_match": True,
        },
        "result_includes": {
            "application_name_filter": GsaActivityLogApplicationNameFilter(
                application_name_to_match=APP_NAME_2,
                match_type=GsaActivityLogMatchType.EXACTMATCHCASEINSENSITIVE,
            )
        },
        "label": "exact app name",
    },
]
application_name_collection = [
    {
        "with_application_names": None,
        "result_includes": {"application_names_collection_filter": Unset},
        "label": "no app names filter",
    },
    {
        "with_application_names": {
            "application_names": [APP_NAME_1, APP_NAME_2],
            "exact_match": False,
        },
        "result_includes": {
            "application_names_collection_filter": GsaActivityLogApplicationNamesCollectionFilter(
                application_names_to_match=[APP_NAME_1, APP_NAME_2],
                collection_match_type=GsaActivityLogCollectionMatchType.COLLECTIONCONTAINS,
            )
        },
        "label": "non-exact app names (two names)",
    },
    {
        "with_application_names": {
            "application_names": [APP_NAME_1],
            "exact_match": False,
        },
        "result_includes": {
            "application_names_collection_filter": GsaActivityLogApplicationNamesCollectionFilter(
                application_names_to_match=[APP_NAME_1],
                collection_match_type=GsaActivityLogCollectionMatchType.COLLECTIONCONTAINS,
            )
        },
        "label": "non-exact app names (one name)",
    },
    {
        "with_application_names": {
            "application_names": [APP_NAME_1, APP_NAME_2],
            "exact_match": True,
        },
        "result_includes": {
            "application_names_collection_filter": GsaActivityLogApplicationNamesCollectionFilter(
                application_names_to_match=[APP_NAME_1, APP_NAME_2],
                collection_match_type=GsaActivityLogCollectionMatchType.COLLECTIONEXACTMATCH,
            )
        },
        "label": "exact app names (two names)",
    },
    {
        "with_application_names": {
            "application_names": [APP_NAME_2],
            "exact_match": True,
        },
        "result_includes": {
            "application_names_collection_filter": GsaActivityLogApplicationNamesCollectionFilter(
                application_names_to_match=[APP_NAME_2],
                collection_match_type=GsaActivityLogCollectionMatchType.COLLECTIONEXACTMATCH,
            )
        },
        "label": "exact app names (one name)",
    },
]
database_key = [
    {
        "with_database_key": None,
        "result_includes": {"database_key_filter": Unset},
        "label": "no db key filter",
    },
    {
        "with_database_key": {
            "database_key": DB_KEY,
            "exact_match": False,
        },
        "result_includes": {
            "database_key_filter": GsaActivityLogDatabaseKeyFilter(
                database_key_to_match=DB_KEY,
                match_type=GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE,
            )
        },
        "label": "non-exact db key",
    },
    {
        "with_database_key": {
            "database_key": DB_KEY,
            "exact_match": True,
        },
        "result_includes": {
            "database_key_filter": GsaActivityLogDatabaseKeyFilter(
                database_key_to_match=DB_KEY,
                match_type=GsaActivityLogMatchType.EXACTMATCHCASEINSENSITIVE,
            )
        },
        "label": "exact db key",
    },
    {
        "with_database_key": {
            "database_key": None,
            "exact_match": True,
        },
        "result_includes": {
            "database_key_filter": GsaActivityLogDatabaseKeyFilter(
                database_key_to_match=None,
                match_type=GsaActivityLogMatchType.EXACTMATCHCASEINSENSITIVE,
            )
        },
        "label": "no db key",
    },
]
dates = [
    {
        "with_date_from": None,
        "with_date_to": None,
        "result_includes": {"date_filter": Unset},
        "label": "no date filter",
    },
    {
        "with_date_from": {
            "date_from": START_DATE,
            "inclusive": True,
        },
        "with_date_to": {
            "date_to": END_DATE,
            "inclusive": True,
        },
        "result_includes": {
            "date_filter": GsaActivityLogDateFilter(
                date_from=at_midnight(START_DATE),
                date_from_inclusive=True,
                date_to=at_midnight(END_DATE),
                date_to_inclusive=True,
            )
        },
        "label": "inclusive start and end date",
    },
    {
        "with_date_from": {
            "date_from": START_DATE,
            "inclusive": False,
        },
        "with_date_to": {
            "date_to": END_DATE,
            "inclusive": True,
        },
        "result_includes": {
            "date_filter": GsaActivityLogDateFilter(
                date_from=at_midnight(START_DATE),
                date_from_inclusive=False,
                date_to=at_midnight(END_DATE),
                date_to_inclusive=True,
            )
        },
        "label": "exclusive start and inclusive end date",
    },
    {
        "with_date_from": {
            "date_from": START_DATE,
            "inclusive": True,
        },
        "with_date_to": {
            "date_to": END_DATE,
            "inclusive": False,
        },
        "result_includes": {
            "date_filter": GsaActivityLogDateFilter(
                date_from=at_midnight(START_DATE),
                date_from_inclusive=True,
                date_to=at_midnight(END_DATE),
                date_to_inclusive=False,
            )
        },
        "label": "inclusive start and exclusive end date",
    },
    {
        "with_date_from": {
            "date_from": START_DATE,
            "inclusive": False,
        },
        "with_date_to": {
            "date_to": END_DATE,
            "inclusive": False,
        },
        "result_includes": {
            "date_filter": GsaActivityLogDateFilter(
                date_from=at_midnight(START_DATE),
                date_from_inclusive=False,
                date_to=at_midnight(END_DATE),
                date_to_inclusive=False,
            )
        },
        "label": "exclusive start and end date",
    },
    {
        "with_date_from": {
            "date_from": START_DATE,
            "inclusive": True,
        },
        "with_date_to": None,
        "result_includes": {
            "date_filter": GsaActivityLogDateFilter(
                date_from=at_midnight(START_DATE),
                date_from_inclusive=True,
                date_to=None,
                date_to_inclusive=False,
            )
        },
        "label": "inclusive start and no end date",
    },
    {
        "with_date_from": {
            "date_from": START_DATE,
            "inclusive": False,
        },
        "with_date_to": None,
        "result_includes": {
            "date_filter": GsaActivityLogDateFilter(
                date_from=at_midnight(START_DATE),
                date_from_inclusive=False,
                date_to=None,
                date_to_inclusive=False,
            )
        },
        "label": "exclusive start and no end date",
    },
    {
        "with_date_to": {
            "date_to": END_DATE,
            "inclusive": True,
        },
        "result_includes": {
            "date_filter": GsaActivityLogDateFilter(
                date_from=None,
                date_from_inclusive=False,
                date_to=at_midnight(END_DATE),
                date_to_inclusive=True,
            )
        },
        "label": "no start and inclusive end date",
    },
    {
        "with_date_to": {
            "date_to": END_DATE,
            "inclusive": False,
        },
        "result_includes": {
            "date_filter": GsaActivityLogDateFilter(
                date_from=None,
                date_from_inclusive=False,
                date_to=at_midnight(END_DATE),
                date_to_inclusive=False,
            )
        },
        "label": "no start and exclusive end date",
    },
]
usage_mode = [
    {
        "with_usage_mode": None,
        "result_includes": {"usage_mode_filter": Unset},
        "label": "no usage mode filter",
    },
    {
        "with_usage_mode": {
            "usage_mode": ActivityUsageMode.EDIT,
        },
        "result_includes": {
            "usage_mode_filter": GsaActivityLogUsageModeFilter(
                usage_mode_to_match=GsaActivityLogUsageMode.EDIT,
            )
        },
        "label": "edit usage mode",
    },
    {
        "with_usage_mode": {
            "usage_mode": ActivityUsageMode.VIEW,
        },
        "result_includes": {
            "usage_mode_filter": GsaActivityLogUsageModeFilter(
                usage_mode_to_match=GsaActivityLogUsageMode.VIEW,
            )
        },
        "label": "view usage mode",
    },
]
username = [
    {"with_username": None, "result_includes": {"username_filter": Unset}, "label": "no username filter"},
    {
        "with_username": {
            "username": USERNAME,
            "exact_match": False,
        },
        "result_includes": {
            "username_filter": GsaActivityLogUsernameFilter(
                username_to_match=USERNAME,
                match_type=GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE,
            )
        },
        "label": "non-exact username",
    },
    {
        "with_username": {
            "username": USERNAME,
            "exact_match": True,
        },
        "result_includes": {
            "username_filter": GsaActivityLogUsernameFilter(
                username_to_match=USERNAME,
                match_type=GsaActivityLogMatchType.EXACTMATCHCASEINSENSITIVE,
            )
        },
        "label": "exact username",
    },
]


def get_parameters():
    """
    Get the cartesian product of filters which can be provided to an ActivityLogFilter object.

    Returns
    -------

    """
    params = []
    for test_case in itertools.product(
        application_name, application_name_collection, database_key, dates, usage_mode, username
    ):
        result_includes = {}
        inputs = {}
        labels = []
        for filter_ in test_case:
            filter_copy = filter_.copy()
            result_includes.update(filter_copy.pop("result_includes"))
            labels.append(filter_copy.pop("label"))
            inputs.update(filter_copy)
        params.append(pytest.param(inputs, result_includes, id=", ".join(labels)))
    return params
