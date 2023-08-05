#!/usr/bin/env python

from distutils.core import setup

setup(name='DesmOEIS',
      version='1.0',
      description='Tool for converting OEIS sequences to Desmos lists',
      author='CascadeIllusion',
      author_email='patrick77000@gmail.com',
      url='https://github.com/CascadeIllusion/DesmOEIS',
      download_url='https://github.com/CascadeIllusion/DesmOEIS/archive/v1.0.tar.gz',
      packages=['DesmOEIS'],
      keywords=['oeis', 'desmos', 'math', 'integers', 'numbers', 'lists', 'conversion'],
      install_requires=[
          'requests',
      ],
     )