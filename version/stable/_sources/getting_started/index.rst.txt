.. _ref_getting_started:

Getting started
###############

.. _ref_software_requirements:

Software requirements
=====================
.. include:: ../../../README.rst
      :start-after: readme_software_requirements
      :end-before: readme_software_requirements_end


Installation
============
.. include:: ../../../README.rst
      :start-after: readme_installation
      :end-before: readme_installation_end


Verify your installation
========================
Check that you can start the PyGranta System client from Python by running this code:

.. code:: python

    >>> from ansys.grantami.system import Connection
    >>> client = Connection("http://my.server.name/mi_servicelayer").with_autologon().connect()
    >>> print(client)

    <SystemApiClient url: http://my.server.name/mi_servicelayer>

This example uses Windows-based autologon authentication. For all supported authentication schemes, see the
:OpenAPI-Common:`OpenAPI-Common documentation <index.html#authentication-schemes>`.

If you see a response from the server, you have successfully installed PyGranta System and
can start using the Granta MI System client. For more examples, see
:ref:`ref_grantami_system_examples`. For comprehensive information on the API, see
:ref:`ref_grantami_system_api_reference`.
