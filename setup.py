#!/usr/bin/env python
from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')

PACKAGES = [
    'web_payments',
    'web_payments_externalpayments',
    # slowly put them into own packages
    'web_payments.authorizenet',
    'web_payments.braintree',
    'web_payments.coinbase',
    'web_payments.cybersource',
    'web_payments.dummy',
    'web_payments.dotpay',
    'web_payments.paypal',
    'web_payments.sagepay',
    'web_payments.sofort',
    'web_payments.stripe',
    'web_payments.wallet']

REQUIREMENTS = [
    'braintree>=3.14.0',
    'Django>=1.11',
    'cryptography>=1.1.0',
    'PyJWT>=1.3.0',
    'requests>=1.2.0',
    'stripe>=1.9.8',
    'suds-jurko>=0.6',
    'xmltodict>=0.9.2']

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
    author='Mirumee Software',
    author_email='hello@mirumee.com',
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
