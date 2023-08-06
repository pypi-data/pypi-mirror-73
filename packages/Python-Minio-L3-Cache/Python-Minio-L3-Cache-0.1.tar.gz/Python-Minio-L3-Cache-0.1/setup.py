#!/usr/bin/env python
import setuptools
from distutils.core import setup

setup(name='Python-Minio-L3-Cache',
      version='0.1',
      description='Simple object-store caching helper library for python3. It uses Pickle for L2 cache and Minio as L3 cache.',
      author='Leonardo Christino',
      author_email='leomilho@gmail.com',
      url='https://github.com/christinoleo/Python-Minio-L3-Cache/',
      packages=['L3MinioCache'],
      license='MIT',
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      )
