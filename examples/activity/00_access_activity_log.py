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

# # Access activity log information

# This example shows how to connect to Granta MI and access the activity log. It shows how to view all activity log
# entries, or how to select entries that meet one or more criteria.

# ## Connect to Granta MI

# Import the ``Connection`` class and create the connection. For more information, see the
# [Basic Usage](../00_Basic_usage.ipynb) example.

# +
from ansys.grantami.system import Connection

connection = Connection("http://my_grantami_server/mi_servicelayer").with_autologon()
client = connection.connect()
# -

# ## Fetch all activity log items

# To fetch all activity log items, use the `get_all_activity_items()` method. The default behavior makes a paged
# request, and returns an iterator.

# <div class="alert alert-info">
#
# **Info:**
#
# Accessing activity log information requires MI_SYSTEM_ADMIN permissions on the Granta MI application server.
# Calling the `get_all_activity_items()` without sufficient permissions will raise a `ApiException` with a 403
# status code.
# </div>

all_logs = client.get_all_activity_items()

# Iterate over the first few items in the response, using `itertools.islice` to slice the iterator:

# +
from itertools import islice

print("Printing first 5...")
for item in islice(all_logs, 5):
    print(
        f"dbkey: {item.database_key}, user: {item.username}, date:{item.activity_date}, "
        f"mode: {item.usage_mode.value}, app names: {item.application_names}"
    )
# -

# ### Iterators and paging

# Iterators and paged API responses are efficient, because the data is only requested at the point at which it is
# required.
#
# However, by design, iterators do not have a defined length. This means calling `len(all_logs)` directly will raise an
# exception. To find the number of items returned, first convert the response to a `list`.
#
# Iterating over an iterator consumes the items iterated over, so first re-run the `get_all_activity_items()` to get a
# fresh iterator.

# +
all_logs = client.get_all_activity_items()  # Initial request fetches the first page of results.

all_logs_list = list(all_logs)  # Exhausts the iterator and stores all items in a list.
# Subsequent pages are fetched via additional requests as the iterator is exhausted.

print(f"{len(all_logs_list)} activity log items in Granta MI.")
# -

# In general though, converting an iterator to a list should be avoided unless necessary.

# The default page size is set to 1000, which should be suitable for most situations.
# To control the page size, use the `page_size` argument:

# +
all_logs_page_size_100 = client.get_all_activity_items(
    page_size=100
)  # Initial request fetches the first page of results.

len(list(all_logs_page_size_100))  # 11 additional requests are made. Each request returns a maximum of 100 results.
# -

# ## Fetch activities for a specific database

# To fetch activities based on one or more criteria, first create an `ActivityLogFilter` object. The
# constructor takes no arguments, and instead is built using a fluent interface. Use the
# `with_database_key()` method to add a filter on the database key.

# +
from ansys.grantami.system import ActivityLogFilter

database_filter = ActivityLogFilter().with_database_key("MI_Corporate_Design_Data")
# -

# Use the `get_activity_items_where()` method to only get items that match the filter.

mi_training_logs = client.get_activity_items_where(database_filter)

# Again, iterate over the first 5 items in the response:

print("Printing first 5...")
for item in islice(mi_training_logs, 5):
    print(
        f"dbkey: {item.database_key}, user: {item.username}, date:{item.activity_date}, "
        f"mode: {item.usage_mode.value}, app names: {item.application_names}"
    )

# Observe that all activity log items contain the requested database key.

# ## Apply a more complex filter

# Create a more complex filter, applying the following criteria:
#
# * The activity was performed by `'USER_5'`.
# * The activity occurred within the first quarter of 2025.
# * The activity was an `EDIT` operation on the `'MI_Corporate_Design_Data'` database.
# * The activity used `'MI Scripting Toolkit'` to make the modification.

# +
from datetime import date

from ansys.grantami.system import ActivityUsageMode

complex_filter = (
    ActivityLogFilter()
    .with_username("USER_5")
    .with_date_from(date.fromisoformat("2025-01-01"), inclusive=True)
    .with_date_to(date.fromisoformat("2025-03-31"), inclusive=True)
    .with_usage_mode(ActivityUsageMode.EDIT)
    .with_database_key("MI_Corporate_Design_Data", exact_match=True)
    .with_application_name("MI Scripting Toolkit")
)

specific_logs = client.get_activity_items_where(complex_filter)
# -
# Again, iterate over the first 5 items in the response. In this case, fewer than 5 items were returned by Granta MI.

for item in islice(specific_logs, 5):
    print(
        f"dbkey: {item.database_key}, user: {item.username}, date:{item.activity_date}, "
        f"mode: {item.usage_mode.value}, app names: {item.application_names}"
    )
