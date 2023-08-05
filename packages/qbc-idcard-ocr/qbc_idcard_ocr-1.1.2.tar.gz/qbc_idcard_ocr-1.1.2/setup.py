#!/usr/bin/env python

from distutils.core import setup

setup(name='qbc_idcard_ocr',
      version='1.1.2',
      description='Recognize ID Card By Ocr.',
      long_description='Recognize ID Card By Ocr.',
      author='charles',
      author_email='charlesmeng@shinelab.cn',
      keywords=['python', 'idcard', 'ocr'],
      url='https://www.shinelab.cn/',
      packages=['qbc_idcard_ocr'],
      package_data={'qbc_idcard_ocr': ['test.jpg', '*.py']},
      license='MIT',
      install_requires=['requests', 'ybc_config', 'opencv-python', 'pillow', 'ybc_exception']
      )