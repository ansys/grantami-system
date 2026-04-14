.. _ref_grantami_system_examples_activity:

.. jinja:: examples

    {% if not build_examples %}
    :orphan:
    {% endif %}


Activity report examples
========================

These examples show how to access and process activity report information.

.. jinja:: examples

    {% if build_examples %}

    .. toctree::
       :maxdepth: 1

       2-1_Access_activity_report
       2-2_Process_activity_report
       2-3_Anonymize_activity_report

    {% endif %}
