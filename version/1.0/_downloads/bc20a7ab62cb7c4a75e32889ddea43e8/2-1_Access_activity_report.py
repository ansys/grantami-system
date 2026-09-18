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

# # Access an activity report

# This example shows how to connect to Granta MI and access the activity report. It shows how to view all activity
# entries, or how to select entries that meet one or more criteria.

# ## Connect to Granta MI

# Import the ``Connection`` class and create the connection. For more information, see the
# [Basic Usage](../1_Basic_usage.ipynb) example.

# +
from ansys.grantami.system import Connection

connection = Connection("http://my_grantami_server/mi_servicelayer").with_autologon()
client = connection.connect()
# -

# ## Fetch activity report

# To fetch the activity report, use the `get_activity_report()` method. This method returns an iterator.

# <div class="alert alert-info">
#
# **Info:**
#
# Accessing activity log information requires MI_SYSTEM_ADMIN permissions on the Granta MI application server.
# Calling the `get_activity_report()` without sufficient permissions will raise a `ApiException` with a 403
# status code.
# </div>

all_items = client.get_activity_report()

# Iterate over the first few items in the response, using `itertools.islice` to slice the iterator:

# +
from itertools import islice

print("Printing first 5...")
for item in islice(all_items, 5):
    print(
        f"dbkey: {item.database_key}, user: {item.username}, date:{item.activity_date}, "
        f"mode: {item.usage_mode.value}, app names: {item.application_names}"
    )
# -

# ### Iterators and paging

# Iterators and paged API responses are efficient, because the data is only requested at the point at which it is
# required.
#
# However, by design, iterators do not have a defined length. This means calling `len(all_items)` directly will raise an
# exception. To find the number of items returned, first convert the response to a `list`.
#
# Iterating over an iterator consumes the items iterated over, so first re-run the `get_activity_report()` to get a
# fresh iterator.

# +
all_items = client.get_activity_report()  # Initial request fetches the first page of results.

all_items_list = list(all_items)  # Exhausts the iterator and stores all items in a list.
# Subsequent pages are fetched via additional requests as the iterator is exhausted.

print(f"{len(all_items_list)} activity report items in Granta MI.")
# -

# In general though, converting an iterator to a list should be avoided unless necessary.

# The default page size is set to 1000, which should be suitable for most situations.
# To control the page size, use the `page_size` argument:

# +
# Initial request fetches the first page of results.
all_items_page_size_100 = client.get_activity_report(page_size=100)

len(list(all_items_page_size_100))  # 11 additional requests are made. Each request returns a maximum of 100 results.
# -

# ## Fetch activities for a specific database

# To fetch activities based on one or more criteria, first create an `ActivityReportFilter` object. The
# constructor takes no arguments, and instead is built using a fluent interface. Use the
# `with_database_key()` method to add a filter on the database key.

# +
from ansys.grantami.system import ActivityReportFilter

database_filter = ActivityReportFilter().with_database_key("MI_Corporate_Design_Data")
# -

# Use the `get_activity_report_where()` method to only get report items that match the filter.

design_data_items = client.get_activity_report_where(database_filter)

# Again, iterate over the first 5 items in the response:

print("Printing first 5...")
for item in islice(design_data_items, 5):
    print(
        f"dbkey: {item.database_key}, user: {item.username}, date:{item.activity_date}, "
        f"mode: {item.usage_mode.value}, app names: {item.application_names}"
    )

# Observe that all activity report items contain the requested database key.

# ## Apply a more complex filter

# Create a more complex filter, applying the following criteria to the activity:
#
# * The activity was performed by `'USER_5'`.
# * The activity occurred within the first quarter of 2025.
# * The activity was an `EDIT` operation on the `'MI_Corporate_Design_Data'` database.
# * The application `'MI Scripting Toolkit'` was used for the activity.

# +
from datetime import date

from ansys.grantami.system import ActivityUsageMode

complex_filter = (
    ActivityReportFilter()
    .with_username("USER_5")
    .with_date_from(date.fromisoformat("2025-01-01"), inclusive=True)
    .with_date_to(date.fromisoformat("2025-03-31"), inclusive=True)
    .with_usage_mode(ActivityUsageMode.EDIT)
    .with_database_key("MI_Corporate_Design_Data", exact_match=True)
    .with_application_name("MI Scripting Toolkit")
)

specific_logs = client.get_activity_report_where(complex_filter)
# -
# Again, iterate over the first 5 items in the response. In this case, fewer than 5 items were returned by Granta MI.

for item in islice(specific_logs, 5):
    print(
        f"dbkey: {item.database_key}, user: {item.username}, date:{item.activity_date}, "
        f"mode: {item.usage_mode.value}, app names: {item.application_names}"
    )
