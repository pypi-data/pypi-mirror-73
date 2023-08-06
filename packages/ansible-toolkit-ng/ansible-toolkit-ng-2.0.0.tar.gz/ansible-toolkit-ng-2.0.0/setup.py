#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import pkg_resources

from setuptools import setup

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(name='ansible-toolkit-ng',
      version='2.0.0',
      description='The missing Ansible tools',
      url='http://github.com/sorrowless/ansible-toolkit-ng',
      author='Stan Bogatkin',
      author_email='stabog.tmb@gmail.com',
      license='GPLv3',
      install_requires=install_requires,
      packages=['ansible_toolkit'],
      scripts=[
          'bin/atk-git-diff',
          'bin/atk-show-vars',
          'bin/atk-show-template',
          'bin/atk-vault',
      ])
