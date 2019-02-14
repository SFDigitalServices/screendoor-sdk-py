"""setup.py for screendoor-sdk"""
# pylint: disable=E0611,F0401
#         No name 'core' in module 'distutils'
#         Unable to import 'distutils.core'
from distutils.core import setup
import setuptools # pylint: disable=unused-import
setup(name='screendoor-sdk',
      version='0.1.0',
      license='MIT',
      author='hui',
      author_email='hui@sfds',
      url='https://github.com/SFDigitalServices',
      packages=["screendoor_sdk"],
      install_requires=[
          'requests'
      ]
      )
