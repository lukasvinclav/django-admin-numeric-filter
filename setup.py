#!/usr/bin/env python
from setuptools import setup

setup(
    name='django-admin-numeric-filter',
    version='0.1.0',
    packages=[
        'admin_numeric_filter',
    ],
    include_package_data=True,
    install_requires=('django', ),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
    ],
    keywords="django admin numeric filter"
)