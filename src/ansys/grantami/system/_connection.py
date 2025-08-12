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

"""
Granta MI System connection module.

Defines the client for interacting with Granta MI.
"""

from abc import ABC
from datetime import timezone
import functools
from typing import Iterator, Optional

from ansys.openapi.common import (
    ApiClient,
    ApiClientFactory,
    ApiException,
    SessionConfiguration,
    generate_user_agent,
)
import requests

from ansys.grantami.serverapi_openapi.v2026r1 import api, models

from ._logger import logger
from ._models import ActivityItem, ActivityReportFilter, _PagedResult

PROXY_PATH = "/proxy/v1.svc/mi"
AUTH_PATH = "/Health/v2.svc"
API_DEFINITION_PATH = "/swagger/v1/swagger.json"
GRANTA_APPLICATION_NAME_HEADER = "PyGranta System"

MINIMUM_GRANTA_MI_VERSION = (26, 1)


def _get_mi_server_version(client: ApiClient) -> tuple[int, ...]:
    """
    Get the Granta MI version as a tuple.

    This method makes direct use of the underlying ``serverapi-openapi`` package.
    The API methods in this package may change over time, and so this method is expected
    to grow to support multiple versions of the ``serverapi-openapi`` package.

    Parameters
    ----------
    client : :class:`~.RecordListApiClient`
        Client object.

    Returns
    -------
    tuple of int
        Granta MI version number.
    """
    schema_api = api.SchemaApi(client)
    server_version_response = schema_api.get_version()
    assert server_version_response.version
    server_version_elements = server_version_response.version.split(".")
    server_version = tuple([int(e) for e in server_version_elements])
    return server_version


class SystemApiClient(ApiClient, ABC):
    """
    Communicates with Granta MI.

    Methods are only implemented if the underlying functionality is supported by the Granta MI server version. If the
    functionality is not available, a :class:`NotImplementedError` is raised.

    This class should not be instantiated directly. New sessions are created with the :class:`.Connection` class.

    Other Parameters
    ----------------
    session : requests.Session
        A requests.Session object.
    service_layer_url : str
        The Granta MI Service Layer URL.
    configuration : ansys.openapi.common.SessionConfiguration
        The configuration to apply to the client.
    """

    def __init__(
        self,
        session: requests.Session,
        service_layer_url: str,
        configuration: SessionConfiguration,
    ):
        self._service_layer_url = service_layer_url
        api_url = service_layer_url + PROXY_PATH

        logger.debug(f"Base Service Layer URL: {self._service_layer_url}")
        logger.debug(f"Service URL: {api_url}")
        super().__init__(session, api_url, configuration)
        self._instantiate_apis()
        self._server_timezone = timezone.utc

    def _instantiate_apis(self) -> None:
        """
        Instantiate the APIs required by this class.

        The versions of the API classes are not fixed, and depend on the api module defined in the ``_api`` class
        variable. This method can be overridden if APIs do not exist for a certain Granta MI version.
        """
        self.schema_api = api.SchemaApi(self)
        self.activity_log_api = api.ActivityLogApi(self)

    def __repr__(self) -> str:
        """Printable representation of the object."""
        return f"<{self.__class__.__name__} url: {self._service_layer_url}>"

    def get_activity_report(self, page_size: Optional[int] = 1000) -> Iterator[ActivityItem]:
        """
        Get all activity information from the Granta MI server.

        Parameters
        ----------
        page_size : int | None, optional
            The number of items to include in a single response. If None, then paging is disabled and all activity
            information will be returned in a single response. Defaults to 1000.

        Returns
        -------
        Iterator of ActivityItem
            An iterator containing the returned activity information.

        Warnings
        --------
        Activity information is updated on the Granta MI server at midnight server time. If a paged request is made
        while the activity report is being updated, duplicate results may be retrieved from the server.

        Avoid making paged requests while the server is updating the activity report.
        """
        gsa_filter = ActivityReportFilter()
        return self.get_activity_report_where(filter_=gsa_filter, page_size=page_size)

    def get_activity_report_where(
        self,
        filter_: ActivityReportFilter,
        page_size: Optional[int] = 1000,
    ) -> Iterator[ActivityItem]:
        """
        Get activity information from the Granta MI server that matches a filter.

        Parameters
        ----------
        filter_ : ActivityReportFilter
            The filter to apply to the request.
        page_size : int | None, optional
            The number of items to include in a single response. If None, then paging is disabled and all activity
            information will be returned in a single response. Defaults to 1000.

        Returns
        -------
        Iterator of ActivityItem
            An iterator containing the returned activity information.

        Warnings
        --------
        Activity information is updated on the Granta MI server at midnight server time. If a paged request is made
        while the activity report is being updated, duplicate results may be retrieved from the server.

        Avoid making paged requests while the server is updating the activity report.
        """
        logger.info("Fetching activity report items...")

        if page_size is not None:
            logger.info(f"Paging options were specified, fetching in batches of size {page_size}...")

            def get_next_page(
                client: "SystemApiClient",
                gsa_filter: models.GsaActivityLogEntriesFilter,
                page: int,
            ) -> list[ActivityItem]:
                _response = client.activity_log_api.get_entries(body=gsa_filter, page_size=page_size, page=page)
                if _response is None:
                    raise ValueError("ActivityLogApi.get_entries must not return None")
                return [ActivityItem._from_model(item) for item in _response.entries]

            partial_func = functools.partial(get_next_page, self, filter_._to_model())
            return _PagedResult(partial_func, ActivityItem)

        logger.info("No paging options were specified, fetching all results...")
        gsa_filter = filter_._to_model()
        response = self.activity_log_api.get_entries(body=gsa_filter)
        if response is None:
            raise ValueError("ActivityLogApi.get_entries must not return None")
        return iter(ActivityItem._from_model(item) for item in response.entries)


class Connection(ApiClientFactory):
    """
    Connects to a Granta MI ServerAPI instance.

    This is a subclass of the :class:`ansys.openapi.common.ApiClientFactory` class. All methods in
    this class are documented as returning :class:`~ansys.openapi.common.ApiClientFactory` class
    instances of the :class:`ansys.grantami.system.Connection` class instead.

    Parameters
    ----------
    servicelayer_url : str
       Base URL of the Granta MI Service Layer application.
    session_configuration : :class:`~ansys.openapi.common.SessionConfiguration`, optional
       Additional configuration settings for the requests session. The default is ``None``, in which
       case the :class:`~ansys.openapi.common.SessionConfiguration` class with default parameters
       is used.

    Notes
    -----
    For advanced usage, including configuring session-specific properties and timeouts, see the
    :external+openapi-common:doc:`ansys-openapi-common API reference <api/index>`. Specifically, see
    the documentation for the :class:`~ansys.openapi.common.ApiClientFactory` base class and the
    :class:`~ansys.openapi.common.SessionConfiguration` class.

    1. Create the connection builder object and specify the server to connect to.
    2. Specify the authentication method to use for the connection and provide credentials if
       required.
    3. Connect to the server, which returns the client object.

    The examples show this process for different authentication methods.

    Examples
    --------
    >>> client = Connection("http://my_mi_server/mi_servicelayer").with_autologon().connect()
    >>> client
    <SystemApiClient: url=http://my_mi_server/mi_servicelayer>
    >>> client = (
    ...     Connection("http://my_mi_server/mi_servicelayer")
    ...     .with_credentials(username="my_username", password="my_password")
    ...     .connect()
    ... )
    >>> client
    <SystemApiClient: url: http://my_mi_server/mi_servicelayer>
    """

    def __init__(self, servicelayer_url: str, session_configuration: Optional[SessionConfiguration] = None):
        from . import __version__

        auth_url = servicelayer_url.strip("/") + AUTH_PATH
        super().__init__(auth_url, session_configuration)
        self._base_service_layer_url = servicelayer_url
        self._session_configuration.headers["X-Granta-ApplicationName"] = GRANTA_APPLICATION_NAME_HEADER
        self._session_configuration.headers["User-Agent"] = generate_user_agent("ansys-grantami-system", __version__)

    def connect(self) -> SystemApiClient:
        """
        Finalize the :class:`.SystemApiClient` client and return it for use.

        Authentication must be configured for this method to succeed.

        Returns
        -------
        :class:`.SystemApiClient`
            Client object that can be used to connect to Granta MI and interact with the Granta MI System API. The
            client object is a subtype of :class:`.SystemApiClient`. The subtype returned depends on the Granta MI
            server version.
        """
        self._validate_builder()
        client = SystemApiClient(
            session=self._session,
            service_layer_url=self._base_service_layer_url,
            configuration=self._session_configuration,
        )
        client.setup_client(models)
        self._test_connection(client)
        return client

    @staticmethod
    def _test_connection(client: SystemApiClient) -> None:
        """
        Check if the created client can be used to perform a request.

        This method tests both that the API definition can be accessed and that the Granta MI
        version is compatible with this package.

        The first checks ensures that the Server API exists and is functional. The second check
        ensures that the Granta MI server version is compatible with this version of the package.

        A failure at any point raises a ``ConnectionError``.

        Parameters
        ----------
        client : :class:`~.SystemApiClient`
            Client object to test.

        Raises
        ------
        ConnectionError
            Error raised if the connection test fails.
        """
        try:
            client.call_api(resource_path=API_DEFINITION_PATH, method="GET")
        except ApiException as e:
            if e.status_code == 404:
                raise ConnectionError(
                    "Cannot find the Server API definition in Granta MI Service Layer. Ensure "
                    "that a compatible version of Granta MI is available and try again."
                ) from e
            else:
                raise ConnectionError(
                    "An unexpected error occurred when trying to connect to the Server API in Granta "
                    " MI Service Layer. Check the Service Layer logs for more information and try "
                    "again."
                ) from e
        except requests.exceptions.RetryError as e:
            raise ConnectionError(
                "An unexpected error occurred when trying to connect to Granta MI Server API. Check "
                "that SSL certificates have been configured for communications between the Granta MI "
                "Server and client Granta MI applications."
            ) from e

        try:
            server_version = _get_mi_server_version(client)
        except ApiException as e:
            # Currently the server version check returns a 403 for a System Admin-only user
            # Suppress this spurious failure by returning early
            if e.status_code == 403:
                return
            raise ConnectionError(
                "Cannot check the Granta MI server version. Ensure that the Granta MI server version "
                f"is at least {'.'.join([str(e) for e in MINIMUM_GRANTA_MI_VERSION])}."
            ) from e

        # Once there are multiple versions of this package targeting different Granta MI server
        # versions, the error message should direct users towards the PyGranta metapackage for
        # earlier versions. This is not necessary now though, because there is no support for
        # versions earlier than 2026 R1.

        if server_version < MINIMUM_GRANTA_MI_VERSION:
            raise ConnectionError(
                f"This package requires a more recent Granta MI version. Detected Granta MI server "
                f"version is {'.'.join([str(e) for e in server_version])}, but this package "
                f"requires at least {'.'.join([str(e) for e in MINIMUM_GRANTA_MI_VERSION])}."
            )
