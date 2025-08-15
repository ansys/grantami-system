import os

from ansys.grantami.system import Connection
from ansys.grantami.system._connection import SystemApiClient
from ansys.grantami.system._models import GrantaMIVersion

# Monkey patch the Connection() class to use the environment variable-specified server URL.
original_ctor = Connection.__init__


def new_init(self: Connection, _):
    original_ctor(self, os.getenv("TEST_SL_URL"))


print("Patching ansys.grantami.system.Connection.__init__")
Connection.__init__ = new_init

# Monkey patch the Connection builder methods to use the environment variable-specified credentials.
Connection.with_creds_original = Connection.with_credentials


def with_credentials(self: Connection, _, __) -> Connection:
    user_name = os.getenv("TEST_USER")
    password = os.getenv("TEST_PASS")
    return self.with_creds_original(user_name, password)


def with_autologon(self: Connection) -> Connection:
    return self.with_credentials("foo", "bar")


print("Patching ansys.grantami.system.Connection.with_credentials")
Connection.with_credentials = with_credentials

print("Patching ansys.grantami.system.Connection.with_autologon")
Connection.with_autologon = with_autologon


# Monkey patch the Client object to report the url specified in the code, or the one below if not
# overridden
server_url = "http://my_grantami_server/mi_servicelayer"


def __repr__(self: SystemApiClient) -> str:  # noqa: N807
    return f"<SystemApiClient url: {server_url}>"


print("Patching ansys.grantami.system.SystemApiClient.__repr__")
SystemApiClient.__repr__ = __repr__


def get_granta_mi_version(self: SystemApiClient) -> GrantaMIVersion:
    return GrantaMIVersion(
        version=(26, 1, 0, 0),
        binary_compatibility_version="26.1.0.0",
    )


print("Patching ansys.grantami.system.SystemApiClient.get_granta_mi_version")
# Required until system admin user can access server version
SystemApiClient.get_granta_mi_version = get_granta_mi_version
