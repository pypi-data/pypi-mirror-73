#!/usr/bin/env python

from distutils.core import setup

setup(name='qbc_food',
      version='1.1.0',
      description='Recognize food image.',
      long_description='To judge a food image or recognize a food image.',
      author='charles',
      author_email='charlesmeng@shinelab.cn',
      keywords=['python', 'food', 'image'],
      url='https://www.shinelab.cn',
      packages=['qbc_food'],
      package_data={'qbc_food': ['test.jpg', '*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config', 'ybc_exception']
      )