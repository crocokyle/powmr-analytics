from setuptools import setup

with open('requirements.txt') as fp:
    requirements = fp.read()

setup(
    name='powmr-analytics',
    install_requires=requirements,
    version='1.0.1',
    packages=['driver'],
    url='https://github.com/crocokyle/powmr-analytics',
    license='GPL-2.0',
    author='CrocoKyle',
    author_email='https://github.com/crocokyle/',
    description='Pulls data from PowMr All-In-One inverters via MODBUS and visualizes the data via InfluxDB'
)
