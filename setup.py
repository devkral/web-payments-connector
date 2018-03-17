#!/usr/bin/env python3
from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')

PACKAGES = [
    'web_payments',
    'web_payments_externalpayments',
    'web_payments_dummy']

REQUIREMENTS = [
    'Django>=1.11',]

TEST_REQUIREMENTS = [
    'pytest',
    'pytest-django'
]
if sys.version_info.major < 3:
    TEST_REQUIREMENTS.append('mock')

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    test_args = []

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='web-payments-connector',
    author='Alexander Kaftan',
    author_email='devkral@web.de',
    description='Universal payment handling for Web Frameworks',
    version='0.12.0',
    url='http://github.com/devkral/web-payments-connector',
    packages=PACKAGES,
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    install_requires=REQUIREMENTS,
    cmdclass={
        'test': PyTest},
    tests_require=TEST_REQUIREMENTS,
    zip_safe=False)
