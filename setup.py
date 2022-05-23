from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='AMAT',
      version='2.2.10',
      description='Aerocapture Mission Analysis Tool',
      url='https://github.com/athulpg007/AMAT',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Athul P. Girija',
      author_email='athulpg007@gmail.com',
      license='GPL-3.0-or-later',
      packages=['AMAT'],
      install_requires=['numpy', 'scipy', 'matplotlib', 'pandas'],
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],


    include_package_data=True,
    
    package_data = {
      'AMAT' : ['data/*'],
      'AMAT' : ['docs/*'],
      'AMAT' : ['examples/*'],
      'AMAT' : ['plots/*'],
      'AMAT' : ['tests/*']
  },
      zip_safe=False)
