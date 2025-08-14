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

# # Process activity log information

# This example shows how to analyze and display activity log information.
#
# This example makes extensive use of the [pandas](https://pandas.pydata.org/)
# and [plotly](https://plotly.com/python/) libraries. Examples using these
# libraries are presented here largely without explanation. Consult the
# documentation for these packages to understand any limitations of the
# approaches demonstrated here, and also how to modify and extend these
# examples.

# ## Fetch activity log information

# Import the ``Connection`` class and create the connection. For more information, see the
# [Basic Usage](../00_Basic_usage.ipynb) example and the
# [Access activity log information](00_access_activity_log.ipynb) example.

# +
from ansys.grantami.system import Connection

connection = Connection("http://my_grantami_server/mi_servicelayer").with_autologon()
client = connection.connect()
items = client.get_all_activity_items()
# -

# ## Process the activity log using a DataFrame

# Prepare the activity log items as a list of dictionaries, where the information for a single
# activity log entry is represented as a dictionary.
#
# Use the `ActivityLogItem.to_dict()` method to create a dictionary for a single item.

rows = [item.to_dict() for item in items]
rows[0]

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
# 4. `database_key`: Convert a `np.NaN` value to the string `"No database"`.

# +
df_processed = df_raw.copy()

# 1. Extract value from enum
df_processed["usage_mode"] = df_raw["usage_mode"].map(lambda x: x.value)

# 2. Flatten application_names
df_processed = df_processed.explode(column="application_names")
df_processed = df_processed.drop_duplicates()

# 3. Convert date to pandas.Timestamp
df_processed["activity_date"] = df_processed["activity_date"].map(lambda x: pd.Timestamp.fromisoformat(x.isoformat()))

# 4. Rename NaN to "No database"
df_processed["database_key"] = df_processed["database_key"].fillna("No database")

df_processed.head()
# -

# The data can be written to an Excel file using the `to_excel()` method.

df_processed.to_excel("activity_data.xlsx")

# ## Plot usasge per month using plotly

# A common use case is to track the unique Granta MI users per month.
#
# Use the `pd.pivot_table()` method to perform a pivot on the data:
# * Specify `username` as the column that contains the values to be plotted.
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

# Alternatively, we can choose to retain the database information, and create a plot of unique users per database per
# month.
#
# Use the `pd.pivot_table()` method again, but add the `database_key` column to the index.

df_activity_per_database_per_month = pd.pivot_table(
    data=df_processed,
    values="username",
    index=["database_key", pd.Grouper(key="activity_date", freq="MS")],
    aggfunc=lambda x: x.nunique(),
)
df_activity_per_database_per_month.head()

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

df_readwrite_per_year = pd.pivot_table(
    data=df_processed,
    values="username",
    index=["usage_mode", pd.Grouper(key="activity_date", freq="YS")],
    aggfunc=lambda x: x.nunique(),
)
df_readwrite_per_year.head()
