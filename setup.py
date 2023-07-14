# -*- coding: utf-8 -*-

from setuptools import setup

DESC = open('README.md').read()

setup(name='fanfou_sdk',
      version='0.0.3',
      description='Fanfou SDK for Python',
      author='LitoMore',
      author_email='litomore@gmail.com',
      url='https://github.com/LitoMore/fanfou-sdk-python',
      packages=['fanfou_sdk'],
      install_requires=['six', 'requests'],
      long_description=DESC,
      long_description_content_type='text/markdown',
      license='MIT',
      platforms=['any'],
      keywords='fanfou')
