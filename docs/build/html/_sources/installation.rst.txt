Installation
=============

Note: AMAT is designed to work with Python 3.0 or greater. You must have a Python 3 installation in your system.

There are three ways to install AMAT. 

Option 1 : Install from pip (recommended)
----------------------------------------------

Note: Python Package Index limits the amount of additional data that can be packaged in the distribution, hence all data cannot be included in the built version. You will need to clone the GitHub repository to get the required data files, examples, and start using AMAT.

**For Linux machines:**

  * ``$ pip install AMAT``
  * ``$ git clone https://github.com/athulpg007/AMAT.git``

If you are unable to clone the repository, you can download the repository as a .zip file from GitHub and extract it. Once AMAT is installed, run an example Jupyter notebook to check everything works correctly.

  * ``$ cd AMAT/examples``
  * ``$ jupyter-notebook``

This will display the full list of example Jupyter notebooks included with AMAT.  Open and run the ``example-01-hello-world`` notebook to get started with AMAT.

**For Windows machines:**

  * ``$ pip install AMAT``

(You must have Anaconda installed. Use the pip command from the Anaconda Prompt terminal). Open a Windows Powershell terminal and clone the GitHub reporistory. You must have Git installed.

  * ``$ git clone https://github.com/athulpg007/AMAT.git``

Run an example Jupyter notebook. From the Anaconda Prompt terminal:

  * ``$ cd AMAT/examples``
  * ``$ jupyter-notebook``

This will display the full list of example Jupyter notebooks included with AMAT. Open and run the ``example-01-hello-world`` notebook to get started with AMAT.


Option 2 : Install from source
-----------------------------------------------

This will clone the repository from GitHub and install AMAT from the source code.

**For Linux machines:**

  * ``$ pip install numpy scipy matplotlib pandas jupyterlab``

Clone the GitHub repository and install AMAT.

  * ``$ git clone https://github.com/athulpg007/AMAT.git``
  * ``$ cd AMAT``
  * ``$ python setup.py install``
  * ``$ cd examples``
  * ``$ jupyter-notebook``

**For Windows machines (from the Anaconda Prompt terminal):**

  * ``$ pip install numpy scipy matplotlib pandas jupyterlab``

Open a Windows Powershell terminal, clone the GitHub repository and install AMAT.

  * ``$ git clone https://github.com/athulpg007/AMAT.git``
  * ``$ cd AMAT``
  * ``$ python setup.py install``
  * ``$ cd examples``
  * ``$ jupyter-notebook``

**To uninstall AMAT:**

1. If you installed AMAT using pip:
  * ``$ pip uninstall AMAT``

2. If you installed AMAT from source, from the main AMAT directory:
  * ``$ python setup.py develop -u``

This will remove the AMAT installation from Python. You may simply delete the root folder where AMAT was installed to completely remove the files.


Option 3 : Install in a virutalenv 
---------------------------------------------------------

If you plan to modifty the source code or add features, the recommended option is to install it in a virtual environment. 

1. Change directory to where you want the virtual environment to be created.
  * ``$ cd home/path``

2. Create a virutal environment and activate it.

**On Linux machines:**

  * ``$ python3 -m venv env1``
  * ``$ source env1/bin/activate``

**On Windows machines (from Anaconda Prompt):**

  * ``$ conda create --name env1``
  * ``$ conda activate env1``
  * ``$ conda install pip``

4. Follow the steps outlined in Option #2 (build from source) to clone the repository and install AMAT. If you make changes to the source code, remove the existing installation, update the setup file with a new version number, and re-install:

  * ``$ python setup.py develop -u``
  * ``$ python setup.py install``

If you want to create a new distrubution package:

  * ``$ python3 setup.py sdist bdist_wheel``

To re-make docs if you made changes to the source code (you must have Sphinx installed):

  * ``$ cd ~root/docs``
  * ``$ sphinx-apidoc -f -o source/ ../``
  * ``$ make html``

If you added a new AMAT module, appropriate changes must be made to docs/source/AMAT.rst.

AMAT Usage
------------

  * ``from AMAT.planet import Planet``
  * ``from AMAT.vehicle import Vehicle``
  * ``from AMAT.launcher import Launcher``
