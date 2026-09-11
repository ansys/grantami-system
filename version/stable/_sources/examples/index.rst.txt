.. _ref_grantami_system_examples:

Examples
========

The following examples demonstrate key aspects of PyGranta System.

To run these examples, install dependencies with this command:

.. code::

   pip install ansys-grantami-system[examples]

And launch ``jupyterlab`` with this command:

.. code::

   jupyter lab


.. jinja:: examples

    {% if build_examples %}

    .. toctree::
       :maxdepth: 2

       1_Basic_usage
       1_Activity/index

    {% else %}

    .. toctree::
       :maxdepth: 2

       test_example

    {% endif %}
