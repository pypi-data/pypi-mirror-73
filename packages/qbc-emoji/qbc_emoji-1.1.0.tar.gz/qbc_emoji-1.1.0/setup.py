#!/usr/bin/env python

from distutils.core import setup

setup(name='qbc_emoji',
      version='1.1.0',
      description='Generateing image using emoji.',
      long_description='Generateing image using emoji.',
      author='charles',
      author_email='charlesmeng@shinelab.cn',
      keywords=['pip3', 'ybc_emoji', 'python3','python','emoji'],
      url='http://www.shinelab.cn/',
      packages = ['qbc_emoji'],
      package_data={'qbc_emoji': ['__init__.py', 'ybc_echarts.py', 'ybc_echarts_unitest.py','NotoSansCJK-Bold.ttc','DejaVuSansMono.ttf']},
      license='MIT',
      install_requires=['ybc_exception', 'pillow']
      )
