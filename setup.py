#!/usr/bin/env python3
from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_payments_dummy.django_dummy.settings.test')

DJANGO_VERSIONS="django>=1.11"

PACKAGES = [
    'web_payments',
    'web_payments.django',
    'web_payments_externalpayments',
    'web_payments_dummy']

REQUIREMENTS = [
    'simplejson>=3.0.0',
    'wtforms<3.0.0',
    # before some people open security holes by handling xml wrong, implement it here and give them only a dict
    # required for xmltodict, if not given it uses the vulnerable implementation as fallback
    'defusedxml>=0.4.1',
    'xmltodict>=0.10.2'
]

TEST_REQUIREMENTS = [
    DJANGO_VERSIONS,
    'pytest',
    'pytest-django'
]

VERSIONING = {
    'root': '.',
    'version_scheme': 'guess-next-dev',
    'local_scheme': 'dirty-tag',
}

EXTRAS={
    'django':  [DJANGO_VERSIONS]
}

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
      license="MIT",
      author='Alexander Kaftan',
      author_email='devkral@web.de',
      description='Universal payment handling for Web Frameworks',
      use_scm_version=VERSIONING,
      setup_requires=['setuptools_scm'],
      url='http://github.com/devkral/web-payments-connector',
      packages=PACKAGES,
      extras_require=EXTRAS,
      include_package_data=True,
      classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'],
      install_requires=REQUIREMENTS,
      cmdclass={
        'test': PyTest},
      tests_require=TEST_REQUIREMENTS,
      zip_safe=False)
