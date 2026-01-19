# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Test Notebook 1

# Check that we can import the Connection class and instantiate some objects.

# + tags=[]
from ansys.grantami.system import Connection

server_url = "http://my_grantami_server/mi_servicelayer"
cxn = Connection(server_url)
cxn
# -
