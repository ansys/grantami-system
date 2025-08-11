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

# +
df_processed = df_raw.copy()
df_processed["usage_mode"] = df_raw["usage_mode"].map(lambda x: x.value)

df_processed = df_processed.explode(column="application_names")
df_processed = df_processed.drop_duplicates()

df_processed["activity_date"] = df_processed["activity_date"].map(lambda x: pd.Timestamp.fromisoformat(x.isoformat()))

df_processed.head()
# -

# ## Unique users per month

# A common use case is to track the unique Granta MI users per month.
#
# First, create a copy of the DataFrame which includes only the columns we are interested in. Also set the index to be
# the `activity_date` column, since this will be the dimension we use for grouping.

df_usernames_by_date = df_processed.drop(["database_key", "usage_mode", "application_names"], axis="columns")
df_usernames_by_date = df_usernames_by_date.set_index("activity_date")
df_usernames_by_date.head()

# Now aggregate the data to retain only unique users for each month. Use a `pd.Grouper()` object with the `ME`
# frequency, which stands for "month end frequency".

df_unique_users_per_month = df_usernames_by_date.groupby(by=pd.Grouper(freq="ME")).nunique()
df_unique_users_per_month.head()

# Finally, plot a histogram using `plotly`. See the plotly documentation for more information on the methods used in the
# cell below.

# +
import plotly.express as px

fig = px.histogram(
    df_unique_users_per_month,
    x=df_unique_users_per_month.index,
    y="username",
    labels={
        "username": "unique users",
        "activity_date": "Month",
    },
)
fig.update_traces(xbins_size="M1")
fig.update_xaxes(showgrid=True, ticklabelmode="period", dtick="M1", tickformat="%b\n%Y")
fig.update_layout(bargap=0.1)

fig.show()
