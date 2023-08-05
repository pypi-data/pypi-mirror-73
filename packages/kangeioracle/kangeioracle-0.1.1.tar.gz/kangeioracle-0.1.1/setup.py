# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='kangeioracle',
    version='0.1.1',
    description='Youkoso module',
    long_description=readme,
    author='Miori Igarashi',
    author_email='miorgash@gmail.com',
    install_requires=['numpy'],
    url='https://github.com/miorgash/kangeioracle',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

