from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='mercuryclient',
      version='0.1a',
      description='Python SDK for Mercury service',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='https://bitbucket.org/esthenos/mercury',
      author='Esthenos Technologies Private Limited',
      author_email='dinu@esthenos.com',
      license='Proprietary License',
      packages=['mercuryclient'],
      install_requires=[
          'requests',
          'PyJWT'
      ],
      zip_safe=False)
