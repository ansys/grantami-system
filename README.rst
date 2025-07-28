PyGranta System
===============

..
   _after-badges


A Python wrapper for Granta MI system administration functions.


Dependencies
------------
.. readme_software_requirements

This version of the ``ansys.grantami.system`` package requires Granta MI 2026 R1 or newer. Use
`the PyGranta documentation <https://grantami.docs.pyansys.com/version/stable/package_versions>`_ to find the
version of this package compatible with older Granta MI versions.

The ``ansys.grantami.system`` package currently supports Python from version 3.11 to version 3.13.

.. readme_software_requirements_end



Installation
--------------
.. readme_installation

To install the latest release from `PyPI <https://pypi.org/project/ansys-grantami-system/>`_, use
this code:

.. code::

    pip install ansys-grantami-system

To install a release compatible with a specific version of Granta MI, use the
`PyGranta <https://grantami.docs.pyansys.com/>`_ meta-package with a requirement specifier:

.. code::

    pip install pygranta==2026.1.0

To see which individual PyGranta package versions are installed with each version of the PyGranta metapackage, consult
the `Package versions <https://grantami.docs.pyansys.com/version/dev/package_versions.html>`_ section of the PyGranta
documentation.

Alternatively, to install the latest development version from ``ansys-grantami-system`` `GitHub <https://github.com/ansys/grantami-system>`_,
use this code:

.. code::

    pip install git+https://github.com/ansys/grantami-system.git


To install a local *development* version with Git and uv, use this code:

.. code::

    git clone https://github.com/ansys/grantami-system
    cd grantami-system
    uv install


The preceding code installs the package and allows you to modify it locally,
with your changes reflected in your Python setup after restarting the Python kernel.

.. readme_installation_end
