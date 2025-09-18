.. _ref_user_guide:

User guide
##########

PyGranta System is a Python client library that allows access to Granta MI system-level functions.

Activity report
---------------

The MI Application Activity Summary report is a rolling monthly summary of user activity in your Granta MI system. The
report includes the following information:

* The date the activity occurred.
* Who performed the activity.
* The MI application and database that were used.
* Whether this was a Read activity, or an Edit activity.

The report is updated daily at midnight server time, with entries for the previous day available once the update
operation has completed. Common activities are merged during the update, such that activity report only contains unique
entries.

The report can be used to determine the number of unique users accessing a Granta MI system within a certain period,
and can be filtered by application, database, and operation type.

The report cannot be used to determine how many times a user accessed the system. The report only shows whether the user
accessed the system or not, along with which applications and databases they used.

See :ref:`ref_grantami_system_examples_activity` for code examples showing how to access and process activity reports,
and
:MI_docs:`Viewing Application Activity information <Granta_MI_Admin_and_Config/mi_admin_and_config/logging_application_activity.html>`
on the Ansys Help Center for more details.
