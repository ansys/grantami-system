# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Getting started
# This example shows how to connect to Granta MI and perform basic operations.

# ## Connect to Granta MI

# First, use the ``ansys.grantami.system.Connection`` class to connect to the Granta MI
# server. The ``Connection`` class uses a fluent interface to build the connection, which is
# always invoked in the following sequence:
#
# 1. Specify your Granta MI Service Layer URL as a parameter to the ``Connection`` class.
# 2. Specify the authentication method using a ``Connection.with_...()`` method.
# 3. Use the ``Connection.connect()`` method to finalize the connection.
#
# This returns a client object, called ``client`` in these examples.

# +
from ansys.grantami.system import Connection

connection = Connection("http://my_grantami_server/mi_servicelayer").with_autologon()
client = connection.connect()
# -

# ## Access activity report
# The activity report describes which users have accessed the Granta MI server. This report lists all user activity in
# the Granta MI system and includes the following information:
#
# * The time an activity occurred
# * Who performed the activity
# * The MI application and database that were used
# * Whether this was a Read activity, or an Edit activity
#
# Use the ``SystemApiClient.get_all_activity_items()`` method to access the report as an iterator of ``ActivityLogItem``
# objects.

items = client.get_all_activity_items()
item = next(items)
print(item)

# For more information about activity reporting information, including how to filter the reports, see the examples.

# ## Access Granta MI version information
# The Granta MI version can be accessed with the ``SystemApiClient.get_granta_mi_version()`` method.

version = client.get_granta_mi_version()
print(version)

# The resulting object supports tuple-style version comparisons.

minimum_version = (25, 2)
print(f"Does version meet minimum requirement? {version > minimum_version}")
