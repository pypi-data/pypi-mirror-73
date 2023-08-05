#!/usr/bin/env python

from distutils.core import setup

setup(name='qbc_bot',
      version='1.0.16',
      description='Smart bot.',
      long_description='Smart bot little ape.',
      author='charles',
      author_email='charlesmeng@shinelab.cn',
      keywords=['python', 'smart bot', 'bot'],
      url='https://www.shinelab.cn/',
      packages=['qbc_bot'],
      package_data={'qbc_bot': ['*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config', 'ybc_exception']
      )
