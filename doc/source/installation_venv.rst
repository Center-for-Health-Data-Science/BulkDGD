Installing with ``virtualenv``
==============================

This section guides you in installing the bulkDGD package in a virtual environment, meaning an instance of Python that is isolated from your system.

This is not strictly necessary, and bulkDGD may be installed system-wide similarly, following steps 4 to 6.

Step 1 - Install ``virtualenv``
-------------------------------

First, check if the ``virtualenv`` Python package is installed in your system. This can be done by verifying whether the ``virtualenv`` command is available.

It is usually available as a package in your distribution if you need to install it. For instance, on Debian-based systems (such as Debian or Ubuntu), it is sufficient to install the ``python-virtualenv`` package.

We recommend installing the ``virtualenv`` package for your local user using ``pip``:

.. code-block:: shell

    pip install --user virtualenv

If the installation is successful, the ``virtualenv`` command will be available.

Step 2 - Create the virtual environment
---------------------------------------

Create your virtual environment in a directory of your choice (in this case, it will be ``./bulkdgd-env``):

.. code-block:: shell

    virtualenv -p /usr/bin/python3.11 bulkdgd-env

You should replace the argument of option ``-p`` according to the location of the Python interpreter you want to use inside the virtual environment.

Step 3 - Activate the environment
---------------------------------

Activate the environment:

.. code-block:: shell

    source bulkdgd-env/bin/activate

Step 4 - Get bulkDGD
--------------------

Download the latest version of bulkDGD from `its GitHub repository <https://github.com/Center-for-Health-Data-Science/bulkDGD/releases/latest>`_. Do not place it inside the environment's directory but in another directory of your choice.

Step 5 - Get the ``dec.pth`` file
---------------------------------

You must download the ``dec.pth`` file containing the trained decoder's parameters before installing bulkDGD, so that the file is copied to the installation directory. The file cannot be shipped together with the GitHub package because of its size, but can be downloaded `here <https://drive.google.com/file/d/1GKMkVmmcEH8glNrQ4092VWYQgq6maYW1/view?usp=sharing>`_. Place it in a directory of your choice.

Once downloaded, place the file into the ``bulkDGD/ioutil/data`` folder before performing the installation.

Step 6 - Install bulkDGD
----------------------------

You can now install bulkDGD using ``pip``.

.. code-block:: shell
    
    pip install ./bulkDGD

bulkDGD should now be installed.

Every time you need to run bulkDGD after opening a new shell, just run step 3 beforehand.
