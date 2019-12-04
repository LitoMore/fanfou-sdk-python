# -*- coding: utf-8 -*-

from setuptools import setup
import fanfou_sdk

DESC = open('README.md').read()

setup(name='fanfou_sdk',
      version='0.0.1',
      description='Fanfou SDK for Python',
      author='LitoMore',
      author_email='litomore@gmail.com',
      url='https://github.com/LitoMore/fanfou-sdk-python',
      packages=['fanfou_sdk'],
      install_requires=['six', 'requests'],
      long_description=DESC,
      license='MIT',
      platforms=['any'],
      keywords='fanfou')
