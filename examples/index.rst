.. _ref_grantami_system_examples:

Examples
========

The following examples demonstrate key aspects of PyGranta System.

.. jinja:: examples

    {% if build_examples %}

    .. toctree::
       :maxdepth: 2

       00_basic_usage

    {% else %}

    .. toctree::
       :maxdepth: 2

       test_example

    {% endif %}
