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

from datetime import date
from typing import Optional

from ansys.grantami.serverapi_openapi.v2026r1 import models

from ._logger import logger


class ActivityLogFilter:
    def __init__(self) -> None:
        pass

    def _to_model(self) -> models.GsaActivityLogEntriesFilter:
        """Generate the DTO for use with the auto-generated client code."""
        logger.debug("Serializing ActivityLogFilter to API model")
        model = models.GsaActivityLogEntriesFilter()
        logger.debug(model.to_str())
        return model


class ActivityLogItem:
    def __init__(
        self,
        date: date,
        application_names: list[str],
        username: str,
        usage_mode: str,
        database_key: Optional[str],
    ) -> None:
        self._date = date
        self._application_names = application_names
        self._username = username
        self._usage_mode = usage_mode
        self._database_key = database_key

    @property
    def date(self) -> date:
        return self._date

    @date.setter
    def date(self, value: date) -> None:
        self._date = value

    @property
    def application_names(self) -> list[str]:
        return self._application_names

    @application_names.setter
    def application_names(self, value: list[str]) -> None:
        self._application_names = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        self._username = value

    @property
    def usage_mode(self) -> str:
        return self._usage_mode

    @usage_mode.setter
    def usage_mode(self, value: str) -> None:
        self._usage_mode = value

    @property
    def database_key(self) -> Optional[str]:
        return self._database_key

    @database_key.setter
    def database_key(self, value: str) -> None:
        self._database_key = value

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
        model:
            DTO object to parse
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
