#!/usr/bin/env python

from setuptools import setup

setup(name='py-gnuplot',
      version='1.1.7',
      keywords = ["gnuplot", "pandas"],
      author='Yongping Guo',
      author_email='guoyoooping@163.com',
      description='py-gnuplot is a python plot tools based on gnuplot.',
      long_description=open('README.rst').read(),
      install_requires = ["pandas"],
      url='http://www.gnuplot.info',
      #url='https://github.com/guoyoooping/py-gnuplot',
      license='GPLv3',
      scripts=[],
      packages=[ 'pygnuplot' ],
      #packages = find_packages(),
      )
