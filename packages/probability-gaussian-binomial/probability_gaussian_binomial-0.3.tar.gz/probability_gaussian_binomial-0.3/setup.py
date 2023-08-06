from setuptools import setup
import sys

with open('./probability_gaussian_binomial/README.md') as f:
    long_description = f.read()

setup(name='probability_gaussian_binomial',
      version='0.3',
      description='Gaussian and binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['probability_gaussian_binomial'],
      author= 'Gopi Mehta',
      author_email= 'gopimehta60@gmail.com',
    zip_safe=False)