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

# # Anonymize an activity report

# This example shows how to anonymize an activity report.

# ## Fetch the activity report

# Import the ``Connection`` class, create the connection, and fetch the activity report. For more
# information, see the [Basic Usage](../1_Basic_usage.ipynb) and
# [Access an activity report](2-1_Access_activity_report.ipynb) examples.

# +
from ansys.grantami.system import Connection

connection = Connection("http://my_grantami_server/mi_servicelayer").with_autologon()
client = connection.connect()
items = client.get_activity_report()
# -

# ## Anonymize the activity report

# `ActivityItem` objects are immutable, and so the `username` for an `ActivityItem` cannot be changed directly.
# However, the `ActivityItem` class is a dataclass, so we can use the `dataclasses.replace()` function to create a new
# object with the required modification.

# +
from dataclasses import replace

anonymized_usernames = {}
anonymized_items = []

for item in items:
    current_username = item.username
    try:
        anonymized_name = anonymized_usernames[current_username]
    except KeyError:
        anonymized_name = f"Anonymous user {len(anonymized_items)}"
        anonymized_usernames[current_username] = anonymized_name

    anonymized_item = replace(item, username=anonymized_name)
    anonymized_items.append(anonymized_item)
# -

# Each item in the activity report now contains an anonymized username. Any analytics that aggregate unique numbers of
# users will produce the same results, but no individual user information will be available.

print(anonymized_items[0])
