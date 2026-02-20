# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0

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
