#!/usr/bin/env python

from distutils.core import setup

setup(name='qbc_face',
      version='1.0.0',
      description='Face detection and analysis.',
      long_description='Face detection and analysis.',
      author='charles',
      author_email='charlesmeng@shinelab.cn',
      keywords=['python', 'face', 'detection', 'recognition'],
      url='https://www.shinelab.cn/',
      packages=['qbc_face'],
      package_data={'qbc_face': ['*.jpg', '*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config', 'ybc_exception']
      )
