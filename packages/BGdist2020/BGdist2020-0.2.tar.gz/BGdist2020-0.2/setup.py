import os
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
dist_dir = [f.path for f in os.scandir(this_directory) if f.is_dir()][0]
with open(path.join(dist_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

    
setup(name='BGdist2020',
      version='0.2',
      description='Gaussian distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['BGdist2020'],
      zip_safe=False)
