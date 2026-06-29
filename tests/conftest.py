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

import pytest
import requests_mock

from .common import (
    _get_connection,
    sl_url,
    sysadmin_password,
    sysadmin_username,
)


@pytest.fixture
def connection_sysadmin():
    return _get_connection(sl_url, sysadmin_username, sysadmin_password)


def pytest_addoption(parser):
    parser.addoption("--mi-version", action="store", default=None)


@pytest.fixture(scope="session")
def mi_version(request):
    mi_version: str = request.config.getoption("--mi-version")
    if not mi_version:
        return None
    parsed_version = mi_version.split(".")
    if len(parsed_version) != 2:
        raise ValueError("--mi-version argument must be a MAJOR.MINOR version number")
    version_number = tuple(int(e) for e in parsed_version)
    return version_number


@pytest.fixture(autouse=True)
def process_integration_marks(request, mi_version):
    """Processes the arguments provided to the integration mark.

    If the mark is initialized with the kwarg ``mi_versions``, the value must be of type list[tuple[int, int]], where
    the tuples contain compatible major and minor release versions of Granta MI. If the version is specified for a test
    case and the Granta MI version being tested against is not in the provided list, the test case is skipped.

    Also handles test-specific behavior, for example if a certain Granta MI version and test are incompatible and need
    to be skipped or xfailed.
    """

    # Argument validation
    if not request.node.get_closest_marker("integration"):
        # No integration marker anywhere in the stack
        return
    if mi_version is None:
        # We didn't get an MI version. If integration tests were requested, an MI version must be provided. Raise
        # an exception to fail all tests.
        raise ValueError(
            "No Granta MI Version provided to pytest. Specify Granta MI version with --mi-version MAJOR.MINOR."
        )

    # Process integration mark arguments
    mark: pytest.Mark = request.node.get_closest_marker("integration")
    if not mark.kwargs:
        # Mark not initialized with any keyword arguments
        return
    allowed_versions = mark.kwargs.get("mi_versions")
    if allowed_versions is None:
        return
    if not isinstance(allowed_versions, list):
        raise TypeError("mi_versions argument type must be of type 'list'")
    if mi_version not in allowed_versions:
        formatted_version = ".".join(str(v) for v in mi_version)
        skip_message = f'Test skipped for Granta MI release version "{formatted_version}"'
        pytest.skip(skip_message)


@pytest.fixture()
def mocker():
    m = requests_mock.Mocker()
    return m
