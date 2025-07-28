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
