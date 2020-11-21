# coding: utf-8

import os
from setuptools import setup
from setuptools import find_packages

import flashback


ROOT = os.path.dirname(__file__)


def read_requirements_file(path):
    path = os.path.join(ROOT, path)

    requirements = []

    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('# '):
                continue

            if line.startswith('-r '):
                requirements += read_requirements_file(line[3:])
            else:
                requirements.append(line)

    return requirements


setup(
    version=flashback.__version__,

    name='flashback',
    author='Paul Renvoisé',
    author_email='renvoisepaul@gmail.com',
    url='https://github.com/PaulRenvoise/flashback',

    description='An utility library for python',
    long_description=open(os.path.join(ROOT, 'README.md'), 'r').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],

    packages=find_packages(exclude=('tests', 'tests.*')),

    install_requires=read_requirements_file('requirements.txt'),
    tests_require=read_requirements_file('requirements-test.txt'),
    python_requires='>=3.6.*',
    setup_requires=['pytest-runner'],

    test_suite='tests',

    entry_points='',
    scripts='',
    data_files=[],
    ext_modules=[],
    cmdclass={},

    license='MIT',
)
