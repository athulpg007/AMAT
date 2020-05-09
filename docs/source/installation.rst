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

On Windows machines, the recommended option is to use Anaconda or Canopy package manager to install these packages.

2. Navigate to the directory where you want AMAT to be installed. Open a terminal (or command window) and use the folllowing command:

  * ``$ cd home/path``

where home/path is to be replaced with the path to the folder where AMAT will be installed. 

3. Clone the github repository using the following command. You must have git installed.

  * ``$ git clone https://github.com/athulpg007/AMAT.git``

If you do not have git installed, you can download a .zip file from the github page and extract it. Copy the entire uncompressed folder into the directory where you want AMAT to be installed.

4. Change directory to AMAT and install package.

  * ``$ cd AMAT``
  * ``$ python setup.py install``

5. Run an example script to check everything is working.

  * ``$ cd examples``
  * ``$ ipython``
  * ``$ run craigLyne2005.py``

(This script will take several seconds to run.)

Option 2 : Install from pip
-----------------------------

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

4. Follow steps 1 through 5 in Option #1 : Install from source.


## Usage

  * ``from AMAT.planet import Planet``
  * ``from AMAT.vehicle import Vehicle``
