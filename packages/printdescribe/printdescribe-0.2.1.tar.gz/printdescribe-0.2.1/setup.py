from setuptools import setup

setup(name = 'printdescribe',
      version = '0.2.1',
      description = 'Print and describe',
      author='Okechukwu Okigbo',
      author_email='okigbookey@gmail.com',
      packages=['printdescribe'], 
      install_requires=['matplotlib',
                          'numpy', 'tabulate'
                          'pandas'], 
      zip_safe = False)