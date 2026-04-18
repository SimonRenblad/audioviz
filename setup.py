#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='audioviz',
      version='0.1',
      # Modules to import from other scripts:
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'audioviz = audioviz.app:main',
        ],
      },
     )
