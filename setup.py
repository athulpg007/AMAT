from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='AMAT',
      version='2.3.0',
      description='Aerocapture Mission Analysis Tool',
      url='https://github.com/athulpg007/AMAT',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Athul P. Girija',
      author_email='athulpg007@gmail.com',
      license='GPL-3.0-or-later',
      packages=['AMAT'],
      install_requires=['numpy==1.26.2', 'scipy==1.11.4', 'matplotlib==3.8.2', 'pandas==2.1.4',
                        'astropy==6.0.0', 'jplephem==2.21'],
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

        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],


    include_package_data=False,

    package_data = {
      'AMAT' : ['tests/*']
  },
      zip_safe=False)
