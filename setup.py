# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


requirements = (
    'setuptools',
)


setup(
    name='samitizer',
    version='0.2.3',
    license='MIT',
    author='Jamie Seol',
    author_email='theeluwin@gmail.com',
    url='https://github.com/theeluwin/samitizer',
    description='Python library for parsing SAMI files.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[],
)
