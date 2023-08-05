from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='registermlmodels',
version='0.1',
description='Register ML Models in Databricks',
url='https://github.com/v1pankaj/register-databricks-ml-models',
author='Pankaj Verma',
author_email='pankaj065@gmail.com',
license='MIT',
packages=['mlmodels'],
install_requires=['mlflow'],
zip_safe=False)