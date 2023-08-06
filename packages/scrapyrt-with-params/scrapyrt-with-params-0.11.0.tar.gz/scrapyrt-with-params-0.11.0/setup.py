# -*- coding: utf-8 -*-
#!/usr/bin/python
from setuptools import setup, find_packages
from os.path import join, dirname

with open(join(dirname(__file__), 'scrapyrt/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name="scrapyrt-with-params",
    version=version,
    author='Manuel Trinidad Garcia',
    author_email='manuel.trinidad.garcia@hotmail.com',
    url="https://github.com/manueltg89/scrapyrt-with-params",
    maintainer='Scrapinghub',
    maintainer_email='manuel.trinidad.garcia@hotmail.com',
    description='Put Scrapy spiders behind an HTTP API',
    long_description=open('README.rst').read(),
    license='BSD',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['scrapyrt = scrapyrt.cmdline:execute']
    },
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: BSD License',
    ],
    install_requires=[
        'Twisted>=14.0.0',
        'Scrapy>=1.0.0',
        'demjson',
        'six>=1.5.2'
    ],
    package_data={
        'scrapyrt': [
            'VERSION',
        ]
    },
)
