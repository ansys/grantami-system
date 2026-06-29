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

from ansys.grantami.system import Connection

from .common import sl_url, sysadmin_password, sysadmin_username

pytestmark = pytest.mark.integration(mi_versions=[(25, 2), (25, 1), (24, 2), (24, 1)])


@pytest.mark.xfail(reason="version check not working for system admin user")
def test_connection_raises_exception(mi_version):
    current_version = ".".join(str(e) for e in mi_version)
    with pytest.raises(
        ConnectionError,
        match=f"This package requires a more recent Granta MI version.*version is {current_version}.*at least 26.1",
    ):
        Connection(sl_url).with_credentials(username=sysadmin_username, password=sysadmin_password).connect()
