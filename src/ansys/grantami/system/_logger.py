# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0

"""Logger module."""

import logging

logger = logging.getLogger("ansys.grantami.system")
logger.addHandler(logging.NullHandler())
