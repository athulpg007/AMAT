Installation
=============

Note: AMAT is currently supported on Python ``3.8``, ``3.9``, and ``3.10``. There are two ways to install AMAT.

Option 1: Install from pip (recommended for most users)
--------------------------------------------------------------------

This is the recommended method if you do not plan or need to make changes
to the source code.

Note: Python Package Index limits the amount of additional data that can be
packaged in the distribution, hence all data cannot be included in the built version.
You will need to clone the GitHub repository to get the required
data files, examples, and start using AMAT.

Create a virtual environment and activate it. It is strongly recommended you install
AMAT inside a virtual environment to prevent it from affecting your global python
packages.

Change directory to where you want the virtual environment to be created.
  * ``$ cd home/path``

**For Linux/MacOS machines:**
  * ``$ python3 -m venv env1``
  * ``$ source env1/bin/activate``

**For Windows machines (from Anaconda prompt):**
  * ``$ conda create --name env1``
  * ``$ conda activate env1``
  * ``$ conda install pip``

Clone the repository and install AMAT:
  * ``$ git clone https://github.com/athulpg007/AMAT.git``
  * ``$ pip install AMAT``

Once AMAT is installed, run an example Jupyter notebook to check everything works correctly.
  * ``$ cd AMAT/examples``
  * ``$ jupyter-notebook``

Note that you will need jupyterlab and pandas (for some examples) to run
the example notebooks. Use ``pip install jupyterlab pandas`` to
install Jupyter and pandas if it is not already installed on your system.
This will display the full list of example Jupyter notebooks included with AMAT.
Open and run the ``example-01-hello-world`` notebook to get started with AMAT.


Option 2: Install from setup.py (recommended for developers)
------------------------------------------------------------------------------

This is the recommended method if you need to make changes to the source code.

Create a virtual environment and activate it
following the steps at the beginning of Option 1.

Clone the GitHub repository and install AMAT using setup.py. The ``-e`` editable flag allows changes you make to take effect when using AMAT.
  * ``$ git clone https://github.com/athulpg007/AMAT.git``
  * ``$ cd AMAT``
  * ``$ python setup.py install -e``
  * ``$ cd examples``
  * ``$ jupyter-notebook``


Note that you will need jupyterlab and pandas (for some examples)
to run the example notebooks. Use ``pip install jupyterlab pandas``
to install Jupyter and pandas if it is not already installed on your system.

If you want to create a new distribution package:
  * ``$ python3 setup.py sdist bdist_wheel``

To build docs locally if you made changes to the source code (you must have the dependencies in ``docs/requirements.txt`` installed):
  * ``$ cd AMAT/docs``
  * ``$ make html``
