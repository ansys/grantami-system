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
"""Models module."""

from datetime import date
from typing import Optional

from ansys.grantami.serverapi_openapi.v2026r1 import models

from ._logger import logger


# TODO: Add filter criteria
class ActivityLogFilter:
    """Filter to use in an activity log operation :meth:`~.SystemApiClient.get_activity_logs_where`."""

    def __init__(self) -> None:
        pass

    def _to_model(self) -> models.GsaActivityLogEntriesFilter:
        """
        Generate the DTO for use with the auto-generated client code.

        Returns
        -------
        models.GsaActivityLogEntriesFilter
            The equivalent filter as a Granta MI Server API model.
        """
        logger.debug("Serializing ActivityLogFilter to API model")
        model = models.GsaActivityLogEntriesFilter()
        logger.debug(model.to_str())
        return model


class ActivityLogItem:
    """
    Describes an activity log item as obtained from the API.

    Read-only - do not directly instantiate or modify instances of this class.

    Other Parameters
    ----------------
    date : datetime.date
        The date on which the activity occurred.
    application_names : list of str
        The application or applications used in the activity.
    username : str
        The user who performed the activity.
    usage_mode : str
        The usage mode associated with the activity.
    database_key : str, optional
        The database key used in the activity.
    """

    def __init__(
        self,
        date: date,
        application_names: list[str],
        username: str,
        usage_mode: str,  # TODO: Make an enum
        database_key: Optional[str],
    ) -> None:
        self.date = date
        self.application_names = application_names
        self.username = username
        self.usage_mode = usage_mode
        self.database_key = database_key

    def __repr__(self) -> str:
        """Printable representation of the object."""
        database_key = f'"{self.database_key}"' if self.database_key else "None"
        repr = (
            f'"<{self.__class__.__name__} date={self.date}, username="{self.username}", database_key={database_key}, '
            f'usage_mode="{self.usage_mode}">"'
        )
        return repr

    @classmethod
    def _from_model(
        cls,
        model: models.GsaActivityLogEntry,
    ) -> "ActivityLogItem":
        """
        Instantiate from a model defined in the auto-generated client code.

        Parameters
        ----------
        model : models.GsaActivityLogEntry
            DTO object to parse.

        Returns
        -------
        ActivityLogItem
            The instantiated object.
        """
        logger.debug("Deserializing ActivityLogItem from API response")
        logger.debug(model.to_str())

        return cls(
            date=model._date.date(),
            application_names=model.application_names,
            username=model.username,
            usage_mode=model.usage_mode.value,
            database_key=model.database_key if model.database_key else None,
        )
