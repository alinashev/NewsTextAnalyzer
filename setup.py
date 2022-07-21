from setuptools import setup, find_packages
import project

setup(
    name='project',
    version=project.__version__,
    author='Alina',
    packages=find_packages(),
)
