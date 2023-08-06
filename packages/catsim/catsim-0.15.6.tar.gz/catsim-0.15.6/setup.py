#!/usr/bin/env python3

from setuptools import setup, find_packages
from catsim import __version__
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Education :: Testing',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)'
    ],
    name='catsim',
    version=__version__,
    description='Computerized Adaptive Testing Simulator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Douglas De Rizzo Meneghetti',
    author_email='douglasrizzom@gmail.com',
    url='https://douglasrizzo.github.io/catsim',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'scipy', 'numexpr', 'matplotlib', 'scikit-learn', 'json_tricks', 'tqdm', 'numpy'
    ],
    extras_require=dict(
        testing=['nose', 'nose-cov', 'sklearn', 'coverage', 'coveralls', 'python-coveralls'],
        docs=[
            'Sphinx', 'numpydoc', 'sphinx_autodoc_annotation', 'sphinx_rtd_theme', 'm2r',
            'bibtex-pygments-lexer', 'matplotlib'
        ]
    ),
    license='LGPLv3'
)
