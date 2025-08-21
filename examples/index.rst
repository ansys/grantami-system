.. _ref_grantami_system_examples:

Examples
========

The following examples demonstrate key aspects of PyGranta System.

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
