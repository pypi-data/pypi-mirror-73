#!/usr/bin/env python

from distutils.core import setup

setup(name='qbc_face_ps',
      version='1.0.0',
      description='Face Control.',
      long_description='Face Control.',
      author='charles',
      author_email='charlesmeng@shinelab.cn',
      keywords=['python', 'face', 'ps'],
      url='http://www.shinelab.cn/',
      packages=['qbc_face_ps'],
      package_data={'qbc_face_ps': ['test.jpg', '*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config', 'ybc_exception']
      )