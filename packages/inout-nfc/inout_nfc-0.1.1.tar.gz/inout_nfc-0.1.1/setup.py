#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

requirements = ['Click>=7.0', 'nfcpy', 'gpiozero', 'requests']

setup_requirements = []

test_requirements = []

setup(
    author="Bram Daams",
    author_email='b.daams@science.ru.nl',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="NFC interface for InOut",
    entry_points={
        'console_scripts': [
            'inout_nfc=inout_nfc.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='inout_nfc',
    name='inout_nfc',
    packages=find_packages(include=['inout_nfc', 'inout_nfc.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/brammeleman/inout_nfc',
    version='0.1.1',
    zip_safe=False
)
