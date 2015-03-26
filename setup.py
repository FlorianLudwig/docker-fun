# -*- coding: utf-8 -*-
from setuptools import setup



setup(
    name="dockerfun",
    version="0.0.1",
    author="Florian Ludwig <f.ludwig@greyrook.com>",
    packages=['dockerfun'],
    install_requires=[
        'docker-py',
        'python-consul',
        'PyYaml'
    ],
    entry_points={
        'console_scripts': [
            'df-compose = dockerfun.cli:compose'
        ]
    }
)