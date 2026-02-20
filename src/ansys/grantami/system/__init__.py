# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0


"""Pythonic client for GRANTA MI System functions."""

import importlib.metadata as importlib_metadata

from ._connection import Connection, SystemApiClient
from ._models import ActivityItem, ActivityReportFilter, ActivityUsageMode, GrantaMIVersion

__all__ = [
    "Connection",
    "SystemApiClient",
    "ActivityReportFilter",
    "ActivityItem",
    "ActivityUsageMode",
    "GrantaMIVersion",
]
__version__ = importlib_metadata.version(__name__.replace(".", "-"))
