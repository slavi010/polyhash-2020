#!/usr/bin/env python

from setuptools import setup
import unittest

# src : https://docs.python.org/3/distutils/setupscript.html
setup(
    name='Polyhash-2020 Solver',
    version='1.0',
    description='Trouver et retourne des solutions pour le polyhash 2020',
    author='Sviatoslav BESNARD, Chama EL MAJENA, Aurelie BOULAIS, Rémis BORIUS',
    author_email='etudiant@slavi.dev',
)


# src : https://stackoverflow.com/questions/17001010/how-to-run-unittest-discover-from-python-setup-py-test/23307488
# def my_test_suite():
#     test_loader = unittest.TestLoader()
#     test_suite = test_loader.discover('tests', pattern='test_*.py')
#     return test_suite
