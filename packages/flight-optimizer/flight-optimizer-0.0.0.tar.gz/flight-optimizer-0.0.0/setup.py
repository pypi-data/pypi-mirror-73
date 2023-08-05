from os.path import abspath, dirname, join
from setuptools import setup, find_packages


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='flight-optimizer',
    version='0.0.0',
    python_requires='>=3.5,<4.0',
    description='Package that searches for the cheapest airplane flights per kilometer.',
    long_description=long_description,
    author='Erik Duisheev',
    author_email='erik.duisheev@gmail.com',
    license='UNLICENSE',
    packages=find_packages(),
    install_requires=[
        'click==7.1.2',
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'flight_optimizer = flight_optimizer.cli:search'
        ],
    }
)
