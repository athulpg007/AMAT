from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='AMAT',
      version='2.0.8',
      description='Aerocapture Mission Analysis Tool',
      url='https://github.com/athulpg007/AMAT',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Athul P. Girija',
      author_email='athulpg007@gmail.com',
      license='cc-by-sa-4.0',
      packages=['AMAT'],
      install_requires=['numpy', 'scipy', 'matplotlib', 'pandas'],
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],


    include_package_data=True,
    
    package_data = {
      'AMAT' : ['data/*'],
      'AMAT' : ['docs/*'],
      'AMAT' : ['examples/*'],
      'AMAT' : ['plots/*']
  },
      zip_safe=False)
