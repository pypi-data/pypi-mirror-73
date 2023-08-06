# -*- coding: utf-8 -*-
from pip._internal.req import parse_requirements
from setuptools import setup, find_packages
from comet_bench import __version__

with open('README.rst') as f:
    readme = f.read()

install_reqs = parse_requirements('requirements.txt', session='')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='comet_bench',
    version=__version__,
    description='An utility to publish benchmarks of Catch2 to Comet ML service',
    long_description=readme,
    author='Aleksey Timin',
    author_email='atimin@gmail.com',
    url='https://github.com/flipback/comet_bench',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires='>=3.3',
    include_package_data=True,
    install_requires=reqs,
    entry_points={
        'console_scripts': ['comet_bench=comet_bench:main']
    }
)
