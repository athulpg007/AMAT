from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='AMAT',
      version='2.2.21',
      description='Aerocapture Mission Analysis Tool',
      url='https://github.com/athulpg007/AMAT',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Athul P. Girija',
      author_email='athulpg007@gmail.com',
      license='GPL-3.0-or-later',
      packages=['AMAT'],
      install_requires=['numpy==1.22.0', 'scipy==1.8.0', 'matplotlib==3.5.2', 'pandas==1.4.2',
                        'astropy>=5.2', 'jplephem==2.17', 'poliastro==0.17'],
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


        'Programming Language :: Python :: 3.9',
    ],


    include_package_data=False,

    package_data = {
      'AMAT' : ['tests/*']
  },
      zip_safe=False)
