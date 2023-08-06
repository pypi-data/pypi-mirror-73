from setuptools import setup

with open('README.md') as f:
    long_description = f.read()
    
setup(name='probability_distribution_func',
      version='0.3',
      description='Gaussian distributions',
      packages=['distributions'],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type="text/markdown",)
