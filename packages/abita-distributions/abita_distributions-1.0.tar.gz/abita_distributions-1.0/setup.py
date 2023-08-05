from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory+'/abita_distributions', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(name='abita_distributions',
      version='1.0',
      description='Gaussian and Binomial distributions',
      packages=['abita_distributions'],
      author='Abita Ann Augustine',
      author_email='abitaaugustine@gmail.com',
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown')
