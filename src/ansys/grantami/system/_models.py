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

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Callable, Iterator, Optional, Self, Type, TypeVar, cast

from ansys.openapi.common import Unset_Type

from ansys.grantami.serverapi_openapi.v2026r1 import models

from ._logger import logger


class ActivityUsageMode(Enum):
    """
    Usage modes for an activity.

    Can be used in :meth:`ActivityReportFilter.with_usage_mode`.
    """

    VIEW = models.GsaActivityLogUsageMode.VIEW.value
    EDIT = models.GsaActivityLogUsageMode.EDIT.value


class ActivityReportFilter:
    r"""
    Builder class to create an activity report filter for use with :meth:`~.SystemApiClient.get_activity_report_where`.

    All text-based fields are always case-insensitive.

    Examples
    --------
    >>> # Activity report for this library only
    >>> pygranta_system_filter = ActivityReportFilter().with_application_name("PyGranta System")
    >>> client.get_activity_report_where(pygranta_system_filter)

    >>> # Activity report relating to the MI_Training database
    >>> mi_training_filter = ActivityReportFilter().with_database_key("MI_Training", exact_match=True)
    >>> client.get_activity_report_where(mi_training_filter)

    >>> # Activity report for a domain user
    >>> domain_user_filter = ActivityReportFilter().with_username("DOMAIN\\user", exact_match=True)
    >>> client.get_activity_report_where(domain_user_filter)

    >>> # Activity report for edit operations using MI Training database using MI Scripting Toolkit, made last month
    >>> first_of_this_month = datetime.date.today().replace(day=1)
    >>> last_of_last_month = first_of_this_month - datetime.timedelta(days=1)
    >>> first_of_last_month = last_of_last_month.replace(day=1)
    >>> combination_filter = (
    ...     ActivityReportFilter()
    ...     .with_application_name("Scripting Toolkit")
    ...     .with_database_key("MI_Training")
    ...     .with_usage_mode(ActivityUsageMode.EDIT)
    ...     .with_date_from(first_of_last_month, inclusive=True)
    ...     .with_date_to(last_of_last_month, inclusive=True)
    ... )
    >>> view_filter.get_activity_report_where(combination_filter)
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

    def __repr__(self) -> str:
        """Printable representation of the object."""
        return f"<{self.__class__.__name__} ...>"

    def with_application_name(self, application_name: str, exact_match: bool = False) -> Self:
        """
        Filter based on a single application name used as part of the activity.

        For filtering based on multiple applications simultaneously, use the :meth:`.with_application_names` method.

        Parameters
        ----------
        application_name : str
            The name of the application used as part of the activity.
        exact_match : bool, optional
            If true, the application name must match exactly, excluding case sensitivity. Defaults to false, in which
            case a partial match is allowed.

        Returns
        -------
        ActivityReportFilter
            The current :class:`.ActivityReportFilter` object.
        """
        # TODO: Think about discovery of application names

        self._application_name_filter = models.GsaActivityLogApplicationNameFilter(
            application_name_to_match=application_name,
            match_type=models.GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE
            if not exact_match
            else models.GsaActivityLogMatchType.EXACTMATCHCASEINSENSITIVE,
        )
        return self

    def with_application_names(self, application_names: list[str], exact_match: bool = False) -> Self:
        """
        Filter based on multiple application names used as part of the activity.

        For partial filtering based on multiple applications simultaneously, use the :meth:`.with_application_names`
        method.

        Parameters
        ----------
        application_names : list of str
            The names of applications used as part of the activity.
        exact_match : bool, optional
            If true, every application name must be involved in the activity for it to be returned. Defaults to false,
            in which case the activity may contain additional application names not specified here.

        Returns
        -------
        ActivityReportFilter
            The current :class:`.ActivityReportFilter` object.
        """
        self._application_names_collection_filter = models.GsaActivityLogApplicationNamesCollectionFilter(
            application_names_to_match=application_names,
            collection_match_type=models.GsaActivityLogCollectionMatchType.COLLECTIONCONTAINS
            if not exact_match
            else models.GsaActivityLogCollectionMatchType.COLLECTIONEXACTMATCH,
        )
        return self

    def with_database_key(self, database_key: str | None, exact_match: bool = False) -> Self:
        """
        Filter based on a database key used as part of the activity.

        If ``database_key = None``, then the ``exact_match`` argument is ignored.

        Parameters
        ----------
        database_key : str or None
            The name of the database key used as part of the activity. To find activities relating to application use
            only, specify :class:`None`.
        exact_match : bool, optional
            If true, the database key must match exactly, excluding case sensitivity. Defaults to false, in which
            case a partial match is allowed.

        Returns
        -------
        ActivityReportFilter
            The current :class:`.ActivityReportFilter` object.
        """
        self._database_key_filter = models.GsaActivityLogDatabaseKeyFilter(
            database_key_to_match=database_key,
            match_type=models.GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE
            if not exact_match and database_key is not None
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
        ActivityReportFilter
            The current :class:`.ActivityReportFilter` object.
        """
        self._date_from = datetime.combine(date_from, datetime.min.time(), tzinfo=None)
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
        ActivityReportFilter
            The current :class:`.ActivityReportFilter` object.
        """
        self._date_to = datetime.combine(date_to, datetime.min.time(), tzinfo=None)
        self._date_to_inclusive = inclusive
        return self

    def with_usage_mode(self, usage_mode: ActivityUsageMode) -> Self:
        """
        Filter based on the usage mode of the activity.

        Parameters
        ----------
        usage_mode : ActivityUsageMode
            The usage mode of the activity.

        Returns
        -------
        ActivityReportFilter
            The current :class:`.ActivityReportFilter` object.
        """
        mode = models.GsaActivityLogUsageMode(usage_mode.value)
        self._usage_mode_filter = models.GsaActivityLogUsageModeFilter(usage_mode_to_match=mode)
        return self

    def with_username(self, username: str, exact_match: bool = False) -> Self:
        """
        Filter based on the username of the user who performed the activity.

        Parameters
        ----------
        username : str
            The username of the user who performed the activity.
        exact_match : bool, optional
            If true, the username must match exactly, excluding case sensitivity.  Defaults to false, in which case a
            partial match is allowed.

        Returns
        -------
        ActivityReportFilter
            The current :class:`.ActivityReportFilter` object.
        """
        self._username_filter = models.GsaActivityLogUsernameFilter(
            username_to_match=username,
            match_type=models.GsaActivityLogMatchType.CONTAINSCASEINSENSITIVE
            if not exact_match
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


@dataclass(frozen=True)
class ActivityItem:
    """
    Describes an activity report item as obtained from the API.

    Read-only dataclass - do not directly instantiate or modify instances of this class.
    """

    activity_date: date
    """The date on which the activity occurred."""
    application_names: list[str]
    """The application or applications used in the activity."""
    username: str
    """The user who performed the activity."""
    usage_mode: ActivityUsageMode
    """The usage mode associated with the activity."""
    database_key: Optional[str]
    """The database key used in the activity."""

    @classmethod
    def _from_model(
        cls,
        model: models.GsaActivityLogEntry,
    ) -> "ActivityItem":
        """
        Instantiate from a model defined in the auto-generated client code.

        Parameters
        ----------
        model : models.GsaActivityLogEntry
            DTO object to parse.

        Returns
        -------
        ActivityItem
            The instantiated object.
        """
        logger.debug("Deserializing ActivityLogItem from API response")
        logger.debug(model.to_str())

        return cls(
            activity_date=model._date.date(),
            application_names=model.application_names,
            username=model.username,
            usage_mode=ActivityUsageMode(model.usage_mode.value),
            database_key=model.database_key if model.database_key else None,
        )


T = TypeVar("T")


class _PagedResult(Iterator[T]):
    """
    Object representing the result of a paged request. Generic subclass of an iterator.

    The individual results are obtained by iterating over this object. The results will be
    fetched from the API as and when they are needed.

    To fetch all the results, execute ``list(PagedResult)``.

    Parameters
    ----------
    next_func : Callable[int, [list[T]]
        The function to be called to retrieve the next page. The function must accept the page number as a single
        argument, and must return a list of result objects.
    iterator_type : Type[T]
        The type of object in the iterator returned by next_func.
    """

    def __init__(
        self,
        next_func: Callable[[int], list[T]],
        iterator_type: Type[T],
    ) -> None:
        self._next_func = next_func
        self._current_page: Iterator[T] = iter([])
        self._page_index = 1
        self._iterator_type = iterator_type

    def __repr__(self) -> str:
        """Printable representation of the object."""
        return f"<{self.__class__.__name__}[{self._iterator_type.__name__}] page_index={self._page_index}>"

    def __iter__(self) -> Self:
        """
        Return the iterator associated with this object.

        Returns
        -------
        Self
            The iterator associated with this object.
        """
        return self

    def __next__(self) -> T:
        """
        Return the next result from the iterator associated with this object.

        Returns
        -------
        T
            The next result from the iterator associated with this object.

        Raises
        ------
        StopIteration
          If there are no more elements.
        """
        try:
            return next(self._current_page)
        except StopIteration:
            next_page = self._next_func(self._page_index)
            self._page_index += 1
            self._current_page = iter(next_page)

        return next(self._current_page)


@dataclass(frozen=True)
class GrantaMIVersion:
    """Information about a Granta MI version."""

    version: tuple[int, ...]
    """The full version number as a n-tuple of integers, where n >= 2."""

    binary_compatibility_version: str
    """The binary compatibility version."""

    @property
    def major_minor_version(self) -> tuple[int, int]:
        """
        The Granta MI version as a 2-tuple of integers. Used to determine API compatibility between versions.

        Returns
        -------
        tuple of int
            The major-minor version as a 2-tuple of ints.
        """
        return cast(tuple[int, int], self.version[:2])

    @classmethod
    def _from_model(cls, model: models.GsaMiVersion) -> "GrantaMIVersion":
        """
        Instantiate from a model defined in the auto-generated client code.

        Parameters
        ----------
        model : models.GsaMiVersion
            DTO object to parse.

        Returns
        -------
        GrantaMIVersion
            The instantiated object.
        """
        if isinstance(model.version, Unset_Type):
            raise TypeError("Property 'version' must not be 'Unset'.")
        version = cls._string_to_tuple(model.version)
        if isinstance(model.binary_compatibility_version, Unset_Type):
            raise TypeError("Property 'binary_compatibility_version' must not be 'Unset'.")
        result = cls(version=version, binary_compatibility_version=model.binary_compatibility_version)
        return result

    @staticmethod
    def _string_to_tuple(version: str) -> tuple[int, ...]:
        """
        Convert a period-separated string to a tuple of integers of at least length 2.

        Parameters
        ----------
        version : str
            A version number described as a period-separated string, e.g. "25.2.1326.0".

        Returns
        -------
        tuple[int, int, *tuple[int, ...]]
            An n-tuple of integers. The number of elements in the tuple depends on the number of elements provided
            in the input.
        """
        version_seq = version.split(".")
        if len(version_seq) < 2:
            raise ValueError(f"Provided version '{version}' is not a valid version string.")
        version_tuple = tuple(int(i) for i in version_seq)
        version_typed = cast(tuple[int, int, *tuple[int, ...]], version_tuple)
        return version_typed

    def __str__(self) -> str:
        """
        Version number as a period-separated string.

        Returns
        -------
        str
            The version number as a string.
        """
        return ".".join(str(i) for i in self.version)
