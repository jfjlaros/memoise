import sys
from setuptools import setup

if sys.version_info < (2, 6):
    raise Exception('memoise requires Python 2.6 or higher.')

# Todo: How does this play with pip freeze requirement files?
requires = ['pylibmc']

# Python 2.6 does not include the argparse module.
try:
    import argparse
except ImportError:
    requires.append('argparse')

import memoise as distmeta

setup(
    name='memoise',
    version=distmeta.__version__,
    description='Memoise decorator.',
    long_description=distmeta.__doc__,
    author=distmeta.__author__,
    author_email=distmeta.__contact__,
    url=distmeta.__homepage__,
    license='MIT License',
    platforms=['any'],
    packages=['memoise'],
    install_requires=requires,
    entry_points = {
        'console_scripts': [
        ]
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
    ],
    keywords='optimisation'
)
