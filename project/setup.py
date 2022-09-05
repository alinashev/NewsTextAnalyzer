from setuptools import setup, find_packages
import commons

setup(
    name='commons',
    version=commons.__version__,
    author='Alina',
    packages=find_packages(),
)
