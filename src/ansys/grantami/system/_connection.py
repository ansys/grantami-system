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
from typing import Iterator, Optional, cast

from ansys.openapi.common import (
    ApiClient,
    ApiClientFactory,
    SessionConfiguration,
    Unset_Type,
    generate_user_agent,
)
import requests

from ansys.grantami.serverapi_openapi.v2026r1 import api, models

from ._logger import logger
from ._models import ActivityLogFilter, ActivityLogItem

PROXY_PATH = "/proxy/v1.svc/mi"
AUTH_PATH = "/Health/v2.svc"
API_DEFINITION_PATH = "/swagger/v1/swagger.json"
GRANTA_APPLICATION_NAME_HEADER = "PyGranta System"


class SystemApiClient(ApiClient, ABC):
    """
    Communicates with Granta MI.

    This is an abstract class. Each concrete subtype of this class corresponds to a specific Granta MI server version.

    Methods are only implemented if the underlying functionality is supported by the Granta MI server version. If the
    functionality is not available, a :class:`NotImplementedError` is raised.
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

    def _instantiate_apis(self) -> None:
        """Instantiate the APIs required by this class.

        The versions of the API classes are not fixed, and depend on the api module defined in the ``_api`` class
        variable. This method can be overridden if APIs do not exist for a certain Granta MI version.
        """
        self.schema_api = api.SchemaApi(self)
        self.activity_log_api = api.ActivityLogApi(self)

    def __repr__(self) -> str:
        """Printable representation of the object."""
        return f"<{self.__class__.__name__} url: {self._service_layer_url}>"

    def _get_mi_server_major_minor_version(self) -> tuple[int, int]:
        """Get the Granta MI major.minor version as a 2-tuple.

        Returns
        -------
        tuple of int
            Granta MI version number.

        """
        server_version_response = self.schema_api.get_version()
        server_version = server_version_response.major_minor_version
        assert not isinstance(server_version, Unset_Type), "'server_version' must not be Unset"
        parsed_version = tuple([int(e) for e in server_version.split(".")])
        return cast(tuple[int, int], parsed_version)

    # TODO: Add paging
    def get_all_activity_logs(self) -> Iterator[ActivityLogItem]:
        """Get all activity logs from the Granta MI server.

        Returns
        -------
        Iterator of ActivityLogItem
            An iterator containing the returned activity log.
        """
        filter = ActivityLogFilter()
        return self.get_activity_logs_where(filter=filter)

    def get_activity_logs_where(self, filter: ActivityLogFilter) -> Iterator[ActivityLogItem]:
        """Get activity logs from the Granta MI server that match a filter.

        Parameters
        ----------
        filter: ActivityLogFilter
            The filter to apply to the request.

        Returns
        -------
        Iterator of ActivityLogItem
            An iterator containing the returned activity log.
        """
        logger.info("Fetching activity log entries...")

        logger.info("No paging options were specified, fetching all results...")
        gsa_filter = filter._to_model()
        response = self.activity_log_api.get_entries(body=gsa_filter)
        assert response is not None, "'response' must not be None"
        return iter(ActivityLogItem._from_model(item) for item in response.entries)


class Connection(ApiClientFactory):
    """
    Connects to a Granta MI ServerAPI instance.

    This is a subclass of the :class:`ansys.openapi.common.ApiClientFactory` class. All methods in
    this class are documented as returning :class:`~ansys.openapi.common.ApiClientFactory` class
    instances of the :class:`ansys.grantami.recordlists.Connection` class instead.

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
        self._session_configuration.headers["User-Agent"] = generate_user_agent(
            "ansys-grantami-recordlists", __version__
        )

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
        return client
