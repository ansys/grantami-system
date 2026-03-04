.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`1.0.0rc0 <https://github.com/ansys/grantami-system/releases/tag/v1.0.0rc0>`_ - March 04, 2026
==============================================================================================

.. tab-set::


  .. tab-item:: Added

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add activitylogapi implementation
          - `#1 <https://github.com/ansys/grantami-system/pull/1>`_

        * - Add get_granta_mi_version() method
          - `#4 <https://github.com/ansys/grantami-system/pull/4>`_

        * - Add examples of get_granta_mi_version and activity report
          - `#5 <https://github.com/ansys/grantami-system/pull/5>`_

        * - Implement ActivityItem as dataclass
          - `#12 <https://github.com/ansys/grantami-system/pull/12>`_

        * - Tech review
          - `#40 <https://github.com/ansys/grantami-system/pull/40>`_


  .. tab-item:: Changed

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Remove option to disable paging
          - `#8 <https://github.com/ansys/grantami-system/pull/8>`_

        * - Change "activity log" references to "activity items" and "activity reports"
          - `#10 <https://github.com/ansys/grantami-system/pull/10>`_

        * - Remove server timezone reference
          - `#11 <https://github.com/ansys/grantami-system/pull/11>`_


  .. tab-item:: Dependencies

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add support for Python 3.10 and 3.14
          - `#34 <https://github.com/ansys/grantami-system/pull/34>`_

        * - Bump nbconvert to v7.17.0 and orjson to 3.11.6
          - `#59 <https://github.com/ansys/grantami-system/pull/59>`_

        * - Prepare 1.0.0rc0 release
          - `#86 <https://github.com/ansys/grantami-system/pull/86>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Initial documentation review
          - `#23 <https://github.com/ansys/grantami-system/pull/23>`_

        * - Add Activity Report to User Guide
          - `#25 <https://github.com/ansys/grantami-system/pull/25>`_

        * - Add documentation for examples extra
          - `#55 <https://github.com/ansys/grantami-system/pull/55>`_

        * - Fix changelog fragments
          - `#88 <https://github.com/ansys/grantami-system/pull/88>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Skip auto-approve for dependabot and pre-commit PRs
          - `#9 <https://github.com/ansys/grantami-system/pull/9>`_

        * - Handle trailing slash on test server URL during test VM warmup
          - `#20 <https://github.com/ansys/grantami-system/pull/20>`_

        * - Use uv run
          - `#48 <https://github.com/ansys/grantami-system/pull/48>`_

        * - Add 2026 R1 test VM
          - `#56 <https://github.com/ansys/grantami-system/pull/56>`_

        * - Standardize uv usage
          - `#58 <https://github.com/ansys/grantami-system/pull/58>`_

        * - Configure dependabot to use uv
          - `#60 <https://github.com/ansys/grantami-system/pull/60>`_

        * - Apply Apache-2.0 license
          - `#79 <https://github.com/ansys/grantami-system/pull/79>`_

        * - Re-enable license check
          - `#81 <https://github.com/ansys/grantami-system/pull/81>`_

        * - Enable codecov upload
          - `#87 <https://github.com/ansys/grantami-system/pull/87>`_


  .. tab-item:: Test

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Test get_granta_mi_version as system administrator
          - `#41 <https://github.com/ansys/grantami-system/pull/41>`_


.. vale on
