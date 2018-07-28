# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


requirements = open('requirements.txt').read()
readme = open('README.md').read() + '\n'
version = open('VERSION').read().strip()

setup(
    name='guillotina_shell',
    version=version,
    description='Guillotina shell',
    long_description=readme,
    author='Steeve Chailloux',
    author_email='steevechailloux@gmail.com',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    url='https://github.com/WnP/guillotina_shell',
    license='MIT',
    setup_requires=[],
    zip_safe=True,
    include_package_data=True,
    package_data={'': ['*.txt', '*.rst']},
    packages=find_packages(),
    # install_requires=requirements,
    extras_require={},
    entry_points={
        "console_scripts": ['gsh = guillotina_shell.main:main']
    },
)
