from setuptools import setup
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

setup(name='gu_bi_dist',
      version='1.0',
      description='Gaussian and Binomial distribution',
      packages=['gu_bi_dist'],
      author = 'Vasanth Kumar',
      author_email = 'vasanth.3656@yahoo.com',
      long_description=read_file('README.md'),
      long_description_content_type='text/markdown',
      zip_safe=False)
