from collections import defaultdict

from ansys.grantami.system import Connection

connection = Connection("http://my_grantami_server/mi_servicelayer").with_autologon()
client = connection.connect()

rows = [item.to_dict() for item in client.get_all_activity_items()]

import pandas as pd

df = pd.DataFrame(rows)

df.usage_mode = df.usage_mode.map(lambda x: x.value)
df = df.explode(column="application_names")  # Flatten out application names in lists
df = df.drop_duplicates()  # Remove resulting duplicates

df["activity_year_month"] = df.activity_date.map(lambda x: f"{x.year}-{x.month}")

# Unique users per month
unique_users_per_month = df.groupby(by="activity_year_month").nunique()

import plotly.express as px

fig = px.bar(unique_users_per_month, x=unique_users_per_month.index, y="username")
fig.show()

# Database usage
users_per_database_key_per_month = df.groupby(by=["database_key", "activity_year_month"])

import plotly.graph_objects as go

data = defaultdict(list)
for (database_key, year_month), new_df in users_per_database_key_per_month:
    data[database_key].append((year_month, new_df["username"].nunique()))

bar_data = []
for database_key, db_data in data.items():
    x = [d[0] for d in db_data]
    y = [d[1] for d in db_data]
    bar = go.Bar(name=database_key, x=x, y=y)
    bar_data.append(bar)

fig = go.Figure(data=bar_data)
# Change the bar mode
fig.update_layout(barmode="stack")
fig.show()

# Pie chart for a single month
idx = pd.IndexSlice
unique_users_per_database_key_last_month = (
    users_per_database_key_per_month.nunique().loc[idx[:, "2025-7"], :].droplevel(level=1)
)
print(unique_users_per_database_key_last_month)

fig = px.pie(
    unique_users_per_database_key_last_month,
    values="username",
    names=unique_users_per_database_key_last_month.index,
)
fig.show()
