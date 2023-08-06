from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(name='super_distributions',
      version='0.1.2',
      author= 'Narayan Sharma',
      author_email= 'narayansharma275@gmail.com',
      description= 'Gaussian and Binomial distributions',
      packages=['super_distributions'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)


