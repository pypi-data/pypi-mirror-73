from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='zmb_distributions',
      version='0.2.5',
      description='Gaussian and binomial distributions',
      long_description=long_description,
      long_description_content_type = 'text/markdown',
      packages=['zmb_distributions'],
      zip_safe=False)
