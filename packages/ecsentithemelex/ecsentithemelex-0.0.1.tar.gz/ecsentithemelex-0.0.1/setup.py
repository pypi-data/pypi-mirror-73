from setuptools import setup, find_packages
from distutils.core import setup

setup(name='ecsentithemelex',
      version='0.0.1',
      description='Russian economic tonal-thematic dictionary',
      url='https://github.com/ilya013/ecsentithemelex',
      packages=find_packages(),
      long_description=open('README.rst').read(),
      include_package_data=True,
      author='Ilya Pyltsin',
      install_requires=[],
      author_email='ilya.pyltsin@gmail.com')

