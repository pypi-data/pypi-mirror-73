#!/usr/bin/env python
# -*- coding: utf-8 -*-
import djangocms_multisite

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = djangocms_multisite.__version__


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='djangocms-multisite',
    version=version,
    description='django-multisite supporto for django CMS',
    long_description=readme + '\n\n' + history,
    author='Iacopo Spalletti',
    author_email='i.spalletti@nephila.it',
    url='https://github.com/nephila/djangocms-multisite',
    packages=[
        'djangocms_multisite',
    ],
    include_package_data=True,
    install_requires=[
        'django-multisite',
        'django-cms',
    ],
    license='BSD',
    zip_safe=False,
    keywords='djangocms-multisite, django',
    test_suite='cms_helper.run',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
