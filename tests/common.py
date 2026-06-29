# Copyright (C) 2025 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import date, datetime
import os

from ansys.grantami.system import Connection, SystemApiClient

sl_url = os.getenv("TEST_SL_URL", "http://localhost/mi_servicelayer")
sysadmin_username = os.getenv("TEST_SYSADMIN_USER")
sysadmin_password = os.getenv("TEST_SYSADMIN_PASS")

ci_unit_tests = os.getenv("CI") and not os.getenv("TEST_SL_URL")
"""If tests are running in CI and the TEST_SL_URL environment variable is not populated, we cannot access MI."""


def _get_connection(url, username, password) -> SystemApiClient | None:
    if ci_unit_tests:
        return None

    if username is not None:
        connection = Connection(servicelayer_url=url).with_credentials(username, password).connect()
    else:
        connection = Connection(servicelayer_url=url).with_autologon().connect()
    return connection


APP_NAME_1 = "test_app_name"
APP_NAME_2 = "app_name_with 😂"
DB_KEY = "test_db_key"
START_DATE = date(year=2022, month=5, day=12)
END_DATE = date(year=2023, month=5, day=12)
USERNAME = r"domain\test_user"


def at_midnight(date_: date) -> datetime:
    "Return a date as a datetime at midnight of that date."

    return datetime.combine(date_, datetime.min.time())
