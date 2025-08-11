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

# ## Fetch activity log information

# Import the ``Connection`` class and create the connection. For more information, see the
# [Basic Usage](../00_Basic_usage.ipynb) example and the
# [Access activity log information](00_access_activity_log.ipynb) example.

# +
from ansys.grantami.system import Connection

connection = Connection("http://my_grantami_server/mi_servicelayer").with_autologon()
client = connection.connect()
items = client.get_all_activity_items()
items
# -

# ## Write activity log information to a dataframe

# Prepare the activity log items as a list of dictionaries, where the information for a single
# activity log entry is represented as a dictionary.
#
# Use the `ActivityLogItem.to_dict()` method to create a dictionary for a single item.

rows = [item.to_dict() for item in client.get_all_activity_items()]
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
df_processed["usage_mode"] = df_raw["usage_mode"].map(lambda x: x.value)

df_processed = df_processed.explode(column="application_names")
df_processed = df_processed.drop_duplicates()

df_processed["activity_date"] = df_processed["activity_date"].map(lambda x: pd.Timestamp.fromisoformat(x.isoformat()))

df_processed["database_key"] = df_processed["database_key"].fillna("No database")

df_processed.head()
# -

# ## Unique users per month

# A common use case is to track the unique Granta MI users per month.
#
# First, create a copy of the DataFrame which includes only the columns we are interested in. Also, set the index to be
# the `activity_date` column, since we will resample the data in this column during the grouping stage.

df_usernames_by_date = df_processed.drop(["database_key", "usage_mode", "application_names"], axis="columns")
df_usernames_by_date = df_usernames_by_date.set_index("activity_date")
df_usernames_by_date.head()

# Next, aggregate the data to retain only unique users for each month. Use a `pd.Grouper()` object with the `MS`
# frequency, which stands for "month start frequency".

df_activity_per_month = df_usernames_by_date.groupby(by=pd.Grouper(freq="MS")).nunique()
df_activity_per_month.head()

# Finally, plot a bar chart the `plotly` express API. See the plotly documentation for more information on the methods
# used in the cell below.

# +
import plotly.express as px

fig = px.bar(
    df_activity_per_month,
    x=df_activity_per_month.index,
    y="username",
    labels={
        "username": "Unique user count",
        "activity_date": "Month",
    },
)
fig.update_xaxes(showgrid=True, dtick="M1", tickformat="%b\n%Y")
fig.update_layout(bargap=0.1)

fig.show()
# -

# ## Unique users per database per month

# Alternatively, we can choose to retain the database information, and create a plot of unique users per database per
# month.
#
# First, create a copy of the DataFrame which includes the `username`, `database_key`, and `activity_data` columns. Set
# the index to be the `activity_date` column.

df_usernames_by_database_and_date = df_processed.drop(["usage_mode", "application_names"], axis="columns")
df_usernames_by_database_and_date = df_usernames_by_database_and_date.set_index("activity_date")
df_usernames_by_database_and_date.head()

# Next, aggregate the data to retain only unique users for each month for each database. Specify both the `database_key`
# column and the `pd.Grouper()` object to group first by `database_key`, then by month.

df_activity_per_database_per_month = df_usernames_by_database_and_date.groupby(
    by=["database_key", pd.Grouper(freq="MS")]
).nunique()

# Since the ``groupby`` contains two groups, the resulting dataframe contains a multi-index with two levels,
# representing the grouping first by `database_key`, and then by `activity_date`.

df_activity_per_database_per_month.head()

# Perform another groupby operation based on the 0th level (by `database_key`), and create a separate bar chart trace
# for each database separately. Then combine the separate traces on a single figure, and set the display mode to
# `"stack"`.
#
# This cell uses the more powerful `graph_objects` API in plotly. See the plotly documentation for more information.

# +
import plotly.graph_objects as go

# Create the figure
fig = go.Figure()

# Iterate over each database key in multi-index level 0, and get the dataframe for each
for database_key, df_activity_per_month in df_activity_per_database_per_month.groupby(level=0):
    trace = go.Bar(
        name=database_key,
        x=df_activity_per_month.index.get_level_values(1),  # Get the dates in muliti-index level 1
        y=df_activity_per_month.username,
    )
    fig.add_trace(trace)

fig.update_xaxes(showgrid=True, dtick="M1", tickformat="%b\n%Y")
fig.update_layout(barmode="stack", bargap=0.1)
fig.show()
# -

# ## Pie chart for a specific month

# +
idx = pd.IndexSlice
unique_users_per_database_key_last_month = df_activity_per_database_per_month.loc[idx[:, "2025-7"], :].droplevel(
    level=1
)
print(unique_users_per_database_key_last_month)

fig = px.pie(
    unique_users_per_database_key_last_month,
    values="username",
    names=unique_users_per_database_key_last_month.index,
)
fig.show()
