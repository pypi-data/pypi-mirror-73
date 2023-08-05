import os
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

    
setup(name='BGdist2020',
      version='0.4',
      author = 'Noel Conlisk',
      description='Gaussian distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['BGdist2020'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
      python_requires='>=3.0',
      zip_safe=False)
