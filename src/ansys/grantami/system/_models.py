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

from datetime import date, datetime, timezone
from typing import Optional, Self

from ansys.grantami.serverapi_openapi.v2026r1 import models

from ._logger import logger


class ActivityLogFilter:
    """
    Filter to use in an activity log operation :meth:`~.SystemApiClient.get_activity_logs_where`.

    All text-based fields are case-insensitive.
    """

    def __init__(self) -> None:
        self._application_name_filter: Optional[models.GsaActivityLogApplicationNameFilter] = None
        self._application_names_collection_filter: Optional[models.GsaActivityLogApplicationNamesCollectionFilter] = (
            None
        )
        self._database_key_filter: Optional[models.GsaActivityLogDatabaseKeyFilter] = None
        self._date_from: Optional[datetime] = None
        self._date_from_inclusive: bool = False
        self._date_to: Optional[datetime] = None
        self._date_to_inclusive: bool = False
        self._usage_mode_filter: Optional[models.GsaActivityLogUsageModeFilter] = None
        self._username_filter: Optional[models.GsaActivityLogUsernameFilter] = None

    def with_application_name(self, application_name: str, case_insensitive_exact_match: bool = False) -> Self:
        """
        Filter based on a single application name used as part of the activity.

        For filtering based on multiple applications simultaneously, use the :meth:`.with_application_names` method.

        Parameters
        ----------
        application_name : str
            The name of the application used as part of the activity.
        case_insensitive_exact_match : bool, optional
            If true, the application name must match exactly. Defaults to false, in which case a partial match is
            allowed.

        Returns
        -------
        ActivityLogFilter
            The current :class:`.ActivityLogFilter` object.
        """
        self._application_name_filter = models.GsaActivityLogApplicationNameFilter(
            application_name_to_match=application_name,
            match_type=models.GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE
            if not case_insensitive_exact_match
            else models.GsaActivityLogMatchType.EXACTMATCHCASEINSENSITIVE,
        )
        return self

    def with_application_names(self, application_names: list[str], case_insensitive_exact_match: bool = False) -> Self:
        """
        Filter based on multiple application names used as part of the activity.

        For partial filtering based on multiple applications simultaneously, use the :meth:`.with_application_names`
        method.

        Parameters
        ----------
        application_names : list of str
            The names of applications used as part of the activity.
        case_insensitive_exact_match : bool, optional
            If true, every application name must be involved in the activity for it to be returned. Defaults to false,
            in which case the activity may contain additional application names not specified here.

        Returns
        -------
        ActivityLogFilter
            The current :class:`.ActivityLogFilter` object.
        """
        self._application_names_collection_filter = models.GsaActivityLogApplicationNamesCollectionFilter(
            application_names_to_match=application_names,
            collection_match_type=models.GsaActivityLogCollectionMatchType.COLLECTIONCONTAINS
            if not case_insensitive_exact_match
            else models.GsaActivityLogCollectionMatchType.COLLECTIONEXACTMATCH,
        )
        return self

    def with_database_key(self, database_key: str | None, case_insensitive_exact_match: bool = False) -> Self:
        """
        Filter based on a database key used as part of the activity.

        Parameters
        ----------
        database_key : str or None
            The name of the database key used as part of the activity. To find activities relating to application use
            only, specify :class:`None`.
        case_insensitive_exact_match : bool, optional
            If true, the database key must match exactly. Defaults to false, in which case a partial match is allowed.

        Returns
        -------
        ActivityLogFilter
            The current :class:`.ActivityLogFilter` object.
        """
        self._database_key_filter = models.GsaActivityLogDatabaseKeyFilter(
            database_key_to_match=database_key,
            match_type=models.GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE
            if not case_insensitive_exact_match
            else models.GsaActivityLogMatchType.EXACTMATCHCASEINSENSITIVE,
        )
        return self

    def with_date_from(self, date_from: date, inclusive: bool = False) -> Self:
        """
        Filter based on the earliest allowed date of the activity.

        Parameters
        ----------
        date_from : datetime.date
            The earliest allowed date of the activity.
        inclusive : bool, optional
            If true, activities occurring on the specified date are allowed. Defaults to false, in which case activities
            occurring on the specified date are not allowed.

        Returns
        -------
        ActivityLogFilter
            The current :class:`.ActivityLogFilter` object.
        """
        self._date_from = datetime.combine(date_from, datetime.min.time(), tzinfo=timezone.utc)
        self._date_from_inclusive = inclusive
        return self

    def with_date_to(self, date_to: date, inclusive: bool = False) -> Self:
        """
        Filter based on the latest allowed date of the activity.

        Parameters
        ----------
        date_to : datetime.date
            The latest allowed date of the activity.
        inclusive : bool, optional
            If true, activities occurring on the specified date are allowed. Defaults to false, in which case activities
            occurring on the specified date are not allowed.

        Returns
        -------
        ActivityLogFilter
            The current :class:`.ActivityLogFilter` object.
        """
        self._date_to = datetime.combine(date_to, datetime.min.time(), tzinfo=timezone.utc)
        self._date_to_inclusive = inclusive
        return self

    def with_usage_mode(self, usage_mode: str) -> Self:
        """
        Filter based on the usage mode of the activity.

        Parameters
        ----------
        usage_mode : str
            The usage mode of the activity.

        Returns
        -------
        ActivityLogFilter
            The current :class:`.ActivityLogFilter` object.
        """
        self._usage_mode_filter = models.GsaActivityLogUsageModeFilter(
            usage_mode_to_match=models.GsaActivityLogUsageMode("edit")
            if usage_mode == "edit"
            else models.GsaActivityLogUsageMode("view"),
        )
        return self

    def with_username(self, username: str, case_insensitive_exact_match: bool = False) -> Self:
        """
        Filter based on the username of the user who performed the activity.

        Parameters
        ----------
        username : str
            The username of the user who performed the activity.
        case_insensitive_exact_match : bool, optional
            If true, the username must match exactly. Defaults to false, in which case a partial match is allowed.

        Returns
        -------
        ActivityLogFilter
            The current :class:`.ActivityLogFilter` object.
        """
        self._username_filter = models.GsaActivityLogUsernameFilter(
            username_to_match=username,
            match_type=models.GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE
            if not case_insensitive_exact_match
            else models.GsaActivityLogMatchType.EXACTMATCHCASEINSENSITIVE,
        )
        return self

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

        if self._date_from is not None or self._date_to is not None:
            model.date_filter = models.GsaActivityLogDateFilter(
                date_from=self._date_from,
                date_to=self._date_to,
                date_from_inclusive=self._date_from_inclusive,
                date_to_inclusive=self._date_to_inclusive,
            )
        if self._application_name_filter:
            model.application_name_filter = self._application_name_filter
        if self._application_names_collection_filter:
            model.application_names_collection_filter = self._application_names_collection_filter
        if self._database_key_filter:
            model.database_key_filter = self._database_key_filter
        if self._usage_mode_filter:
            model.usage_mode_filter = self._usage_mode_filter
        if self._username_filter:
            model.username_filter = self._username_filter

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
