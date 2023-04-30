Testing
=======

Support for unit tests and system tests are provided. The unit tests are written using python's ``unittest`` package. These are located in the ``tests/unit`` directory. We can invoke them with the standard ``unittest`` commands, e.g.

.. code-block:: bash

    python3 -m unittest discover -s tests/unit

Apart from unit tests, some system tests are also provided which are slow and intended to be used to check that OpenFOAM can actually use the provided case setups. These are located in the ``tests/system`` directory. To run the system tests, we need to run the following python file

.. code-block:: bash

    python3 tests/system/SystemTestManager.py

Within this file, there is a variable called ``of_versions`` defined at the top of the file, which contains the version identifiers of OpenFOAM that shoudl be tested. This allows us to install different versions of OpenFOAM and test that the generated cases will work for any of the installed versions. We can also run the above system tests with the flag ``--latestVersionOnly``, which will only runt he system tests with the latest version of OpenFOAM defined in the ``of_versions`` variable. The command would look as the following

.. code-block:: bash

    python3 tests/system/SystemTestManager.py --latestVersionOnly