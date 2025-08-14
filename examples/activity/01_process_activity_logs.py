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

# # Process an activity report

# This example shows how to analyze and display an activity report.
#
# This example makes extensive use of the [pandas](https://pandas.pydata.org/)
# and [plotly](https://plotly.com/python/) libraries. Examples using these
# libraries are presented here largely without explanation. Consult the
# documentation for these packages to understand any limitations of the
# approaches demonstrated here, and also how to modify and extend these
# examples.

# ## Fetch the activity report

# Import the ``Connection`` class, create the connection, and fetch the activity report for the
# 12 months between July 2024 and June 2025. For more information, see the
# [Basic Usage](../00_Basic_usage.ipynb) and [Access an activity report](00_access_activity_log.ipynb)
# examples.

# +
from datetime import date

from ansys.grantami.system import ActivityReportFilter, Connection

connection = Connection("http://my_grantami_server/mi_servicelayer").with_autologon()
client = connection.connect()
date_filter = (
    ActivityReportFilter()
    .with_date_from(date.fromisoformat("2024-07-01"), inclusive=True)
    .with_date_to(date.fromisoformat("2025-06-30"), inclusive=True)
)
items = client.get_activity_report_where(date_filter)
# -

# ## Process the activity report using a DataFrame

# Prepare the activity report items as a list of dictionaries, where the information for a single
# activity log entry is represented as a dictionary.
#
# ActivityItem is a dataclass, so use the standard library `dataclasses.asdict()` function to create a dictionary for
# each item.

# +
from dataclasses import asdict

rows = [asdict(item) for item in items]
rows[0]
# -

# Now use this data representation to create a dataframe:

# +
import pandas as pd

df_raw = pd.DataFrame(rows)
df_raw.head()
# -

# Process the data:
#
# 1. `usage_mode`: Extract the value from the Enum using `DataFrame.map()`.
# 2. `application_names`: Flatten the structure using `DataFrame.explode()` and `DataFrame.drop_duplicates()`.
# 3. `activity_date`: Convert the builtin `datetime.date` object to the more powerful `pandas.Timestamp` object.

# +
df_processed = df_raw.copy()

# 1. Extract value from enum
df_processed["usage_mode"] = df_raw["usage_mode"].map(lambda x: x.value)

# 2. Flatten application_names
df_processed = df_processed.explode(column="application_names")
df_processed = df_processed.drop_duplicates()

# 3. Convert date to pandas.Timestamp
df_processed["activity_date"] = df_processed["activity_date"].map(lambda x: pd.Timestamp.fromisoformat(x.isoformat()))

df_processed.head()
# -

# The data can be written to an Excel file using the `to_excel()` method.

df_processed.to_excel("activity_data.xlsx")

# ## Aggregated usage by month

# A common use case is to track the unique Granta MI users per month.
#
# Use the `pd.pivot_table()` method to perform a pivot on the data:
# * Specify `username` as the column that contains the values of interest.
# * Use a `pd.Grouper()` object for the index. Use the `MS` frequency to group the `activity_date` column by month.
# * Use `nunique()` to count the unique `username` values in each `activity_date` group.
#
# For a more detailed description of `pivot_table()`, `Grouper()`, and `nunique()`, consult the pandas documentation.

df_activity_per_month = pd.pivot_table(
    data=df_processed,
    values="username",
    index=pd.Grouper(key="activity_date", freq="MS"),
    aggfunc=lambda x: x.nunique(),
)
df_activity_per_month.head()

# Finally, plot a bar chart the `plotly` express API. See the plotly documentation for more information on the methods
# used in the cell below.

# +
import plotly.express as px

fig = px.bar(
    df_activity_per_month,
    x=df_activity_per_month.index,
    y="username",
    title="Unique users per month",
    labels={
        "username": "Unique user count",
        "activity_date": "Month",
    },
)
fig.update_xaxes(showgrid=True, dtick="M1", tickformat="%b\n%Y")
fig.update_layout(bargap=0.1)

fig.show()
# -

# ## Aggregated usage by month and database

# Alternatively, include the database key in the pivot to create a plot of unique users per database per month.
#
# First, filter out rows which do not relate to a particular database. Then, use the `pd.pivot_table()` method
# again, but add the `database_key` column to the index.

# +
df_database_rows = df_processed[df_processed["database_key"].notnull()]

df_activity_per_database_per_month = pd.pivot_table(
    data=df_database_rows,
    values="username",
    index=["database_key", pd.Grouper(key="activity_date", freq="MS")],
    aggfunc=lambda x: x.nunique(),
)
df_activity_per_database_per_month.head()
# -

# Iterate over each sub-frame grouped by the `database_key` index level, and create a separate bar chart trace
# for each. Then combine the separate traces on a single figure, and set the display mode to `"stack"`.
#
# This cell uses the more powerful `graph_objects` API in plotly. See the plotly documentation for more information.

# +
import plotly.graph_objects as go

# Create the figure
fig = go.Figure()

# Iterate over each value in the "database_key" index level
for database_key, df_activity_per_month in df_activity_per_database_per_month.groupby("database_key"):
    trace = go.Bar(
        name=database_key,
        x=df_activity_per_month.index.get_level_values("activity_date"),
        y=df_activity_per_month.username,
    )
    fig.add_trace(trace)

fig.update_xaxes(title="Month", showgrid=True, dtick="M1", tickformat="%b\n%Y")
fig.update_yaxes(title="Unique user count")
fig.update_layout(title="Unique users per month, grouped by database", barmode="stack", bargap=0.1)
fig.show()
# -

# ## Aggregated usage by usage mode

# A different way of grouping users is by whether they are read or write users of Granta MI.
#
# <div class="alert alert-info">
#
# **Info:**
#
# The usage mode is only available on activity report items created by Granta MI 2026 R1 and later. All activity report
# items created by Granta MI 2025 R2 and earlier are returned as 'view' activities.
# </div>
#
# First, use the `pd.pivot_table()` method to perform a pivot on the data:
# * Specify `username` as the column that contains the values of interest.
# * Specify `usage_mode` as the index to group the data by usage mode.
# * Use `unique()` to return the unique usernames in each usage mode group.
#
# Next, subtract the set of 'edit' users from the set of 'view' users. This avoids double-counting users who both edit
# and view data.
#
# Finally, calculate the length of each set of users by using `.apply()` to apply the `len()` function to each cell.

df_by_usage_mode = df_processed.pivot_table(
    values="username",
    index="usage_mode",
    aggfunc=lambda x: set(x.unique()),
)
# The 'view' column in df_by_usage_mode now contains sets of users in each group
df_by_usage_mode.loc["view"] = df_by_usage_mode.loc["view"] - df_by_usage_mode.loc["edit"]
df_by_usage_mode["username"] = df_by_usage_mode["username"].apply(len)
df_by_usage_mode

# Plot a bar chart the `plotly` express API.

fig = px.bar(
    df_by_usage_mode,
    x=df_by_usage_mode.index,
    y="username",
    title="Unique users by usage mode",
    labels={
        "username": "Unique user count",
        "usage_mode": "Usage mode",
    },
)
fig.show()
