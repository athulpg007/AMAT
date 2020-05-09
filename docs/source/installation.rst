Installation
=============


Note: AMAT is designed to work with Python 3.0 or greater. You must have a Python 3 installation in your system.

There are three ways to install AMAT. 

Option 1 : Install from source (recommended)
----------------------------------------------

This allows you to download the "entire" package (with the required data files to run examples).

1. Make sure you have numpy, scipy, matplotlib and pandas installed. Most likely you already have these installed. If not, use the following commands to install these dependenies first. Open a terminal window (on Linux/Mac machines) and type the following commands. You must have pip installed.

  * ``$ pip install numpy`` 
  * ``$ pip install scipy``
  * ``$ pip install matplotlib``
  * ``$ pip install pandas``

It is recommeded to have `Jupyter Notebook`_ installed to run the example notebooks.

  * ``pip install jupyterlab``

.. _Jupyter Notebook: https://jupyter.org/index.html

On Windows machines, the recommended option is to use  `Anaconda`_ package manager to install these packages.

.. _Anaconda: https://www.anaconda.com/ 

2. Navigate to the directory where you want AMAT to be installed. Open a terminal (or command window) and use the folllowing command:

  * ``$ cd home/path``

where home/path is to be replaced with the path to the folder where AMAT will be installed. 

3. Clone the github repository using the following command. You must have git installed.

  * ``$ git clone https://github.com/athulpg007/AMAT.git``

If you do not have git installed, you can download a .zip file from the github page and extract it. Copy the entire uncompressed folder into the directory where you want AMAT to be installed.

4. Change directory to AMAT and install package.

  * ``$ cd AMAT``
  * ``$ python setup.py install``

5. Check that you have the required data files. For example, in the root folder where AMAT is installed, you should see a folder names atmdata with data for various planets.

6. Run an example script to check everything is working.

  * ``$ cd examples``
  * ``$ ipython``
  * ``$ run example-01-hello-world.py``

To uninstall AMAT, use

  * ``python setup.py develop -u``

This will remove the AMAT installation from Python. You may simply delete the root folder where AMAT was installed to completely remove the files.

Option 2 : Install from pip (NOT recommended)
-----------------------------------------------

This allows you to download the package, but without most of the data files. You can run the program, but will need to visit the git repository later to download some of the data files and place them in an appropriate location. You will also need to change the location of data files in the example scripts if you use them. 

Python Package Index limits the amount of additional data that can be packaged in the distribution, hence all data cannot be included in the built version.

  * ``$ pip install AMAT``

Option 3 : Install in a virutalenv (for developers)
---------------------------------------------------------

If you plan to test or develop the package, the recommended option is to to install it in a virtual environment. This allows you to discard changes and start afresh without having to do a system-wide installation.

1. Change directory to where you want the virtual environment to be created.

  * ``$ cd home/path``

2. Create a virutal environment and activate it.

  * ``$ python3 -m venv env1``
  * ``$ source env1/bin/activate``

3. Change directory to env1

  * ``$ cd env1``

4. Follow steps 1 through 6 in Option #1 : Install from source. pip will automatically fetch the required dependencies.


5. If you make changes to the source code, use 

 * ``python setup.py develop -u``

to remove the previously installed version. Re-install using

 * ``$ python setup.py install``

6. To create a distribution

 * ``python3 setup.py sdist bdist_wheel``

7. To re-make docs if you made changes to the source code, you must have sphinx installed.

 * ``cd ~root/docs``
 * ``sphinx-apidoc -f -o source/ ../``
 * ``make html``

If you added a new AMAT module, appropriate changes must be made to docs/source/AMAT.rst.

AMAT Usage
------------

  * ``from AMAT.planet import Planet``
  * ``from AMAT.vehicle import Vehicle``
  * ``from AMAT.launcher import Launcher``
