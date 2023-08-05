from setuptools import setup
import setuptools

setuptools.setup(
    # setup(
    name='python_forex_quotes',
    version='2.0.1',
    description='Forex quote wrapper for 1Forge.com',
    long_description='Python library to fetch and parse realtime Forex quotes and convert currencies from 1Forge.com',
    url='https://github.com/1forge/python-forex-quotes/',
    keywords='forex currency trading api',
    author='1Forge',
    author_email='contact@1forge.com',
    license='MIT',
    # packages=['python_forex_quotes'],
    # packages=setuptools.find_packages(),
    packages=setuptools.find_packages(
        include=['python_forex_quotes', 'python_forex_quotes.*']),
    python_requires='>=3.7',
    zip_safe=False)
