"""
A Python wrapper for Stanford CoreNLP's SUTime
for french language. Forked from Frable repository

See:
nlp.stanford.edu/software/zodiac-sutime.shtml
"""

from io import open
from os import path

from setuptools import setup
THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with open(path.join(THIS_DIRECTORY, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='zodiac-sutime',
    version='1.0.0',
    description='A Python wrapper for Stanford CoreNLP\'s SUTime',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/Remydeme/zodiac-sutime',
    author='Deme Rémy',
    author_email='demeremy@gmail.com',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Linguistic'
    ],
    keywords='stanford corenlp zodiac-sutime datetime parser parsing nlp',
    packages=['zodiac-sutime'],
    install_requires=[
        'JPype1>=0.6.0'
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'aniso8601',
        'pytest',
        'python-dateutil'
    ],
    package_data={
        'zodiac-sutime': [
            'jars/stanford-corenlp-zodiac-sutime-python-1.4.0.jar',
            'jars/stanford-corenlp-3.9.2-models-french.jar',
            ''
        ],
    },
    package_dir={'zodiac-sutime': 'zodiac-sutime'},
    include_package_data=True,
    zip_safe=False
)
