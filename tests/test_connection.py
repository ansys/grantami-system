# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0

import re

import pytest
import requests.exceptions
import requests_mock

from ansys.grantami.system import Connection, SystemApiClient
from ansys.grantami.system._connection import (
    AUTH_PATH,
    PROXY_PATH,
)


@pytest.fixture
def sl_url():
    return "http://host/path"


@pytest.fixture
def successful_auth(mocker, sl_url):
    with mocker:
        mocker.get(sl_url)
        mocker.get(sl_url + AUTH_PATH)


def test_missing_api_definition_raises_informative_error(sl_url, successful_auth, mocker):
    with mocker:
        service_matcher = re.compile(f"{sl_url}{PROXY_PATH}.*")
        mocker.get(service_matcher, status_code=404)
        with pytest.raises(
            ConnectionError,
            match="Cannot find the Server API definition in Granta MI Service Layer",
        ):
            Connection(sl_url).with_anonymous().connect()


def test_unhandled_test_connection_response_raises_informative_error(sl_url, successful_auth, mocker):
    with mocker:
        service_matcher = re.compile(f"{sl_url}{PROXY_PATH}.*")
        mocker.get(service_matcher, status_code=500)
        with pytest.raises(ConnectionError, match="An unexpected error occurred"):
            Connection(sl_url).with_anonymous().connect()


def test_500_on_test_connection_is_handled(sl_url, successful_auth, mocker):
    with mocker:
        connection = Connection(sl_url).with_anonymous()
        mocker.get(requests_mock.ANY, exc=requests.exceptions.RetryError)
        with pytest.raises(ConnectionError, match="Check that SSL certificates have been configured"):
            connection.connect()


def test_new_server_version(sl_url, successful_auth, mocker):
    mi_version_response = {
        "binaryCompatibilityVersion": "26.1.0.0",
        "version": "26.1.820.0",
        "majorMinorVersion": "26.1",
    }

    with mocker:
        connection = Connection(sl_url).with_anonymous()
        mocker.get(requests_mock.ANY, status_code=200, json=mi_version_response)
        client = connection.connect()
    assert isinstance(client, SystemApiClient)


def test_old_unsupported_server_version_is_handled(sl_url, successful_auth, mocker):
    mi_version_response = {
        "binaryCompatibilityVersion": "24.2.0.0",
        "version": "24.2.2.3",
        "majorMinorVersion": "24.2",
    }

    with mocker:
        connection = Connection(sl_url).with_anonymous()
        mocker.get(requests_mock.ANY, status_code=200, json=mi_version_response)
        with pytest.raises(
            ConnectionError,
            match=r"This package requires a more recent Granta MI version.*24\.2.*26\.1",
        ):
            connection.connect()


def test_server_version_error_is_handled(sl_url, successful_auth, mocker):
    with mocker:
        connection = Connection(sl_url).with_anonymous()
        mocker.get(requests_mock.ANY, status_code=200, json={})
        version_path = re.compile("schema/mi-version")
        mocker.get(version_path, status_code=404)
        with pytest.raises(
            ConnectionError,
            match=r"Cannot check the Granta MI server version",
        ):
            connection.connect()


def test_unauthorized_version_check_is_ignored(sl_url, successful_auth, mocker):
    with mocker:
        connection = Connection(sl_url).with_anonymous()
        mocker.get(requests_mock.ANY, status_code=200, json={})
        version_path = re.compile("schema/mi-version")
        mocker.get(version_path, status_code=403)
        connection.connect()
