from setuptools import setup
import setuptools

setup(name='dexterous_gym',
      version='0.1.2',
      description='Challenging extensions to openAI Gyms hand manipulation environments',
      url='http://github.com/henrycharlesworth/dexterous_gym',
      author='Henry Charlesworth',
      author_email='H.Charlesworth@warwick.ac.uk',
      packages=setuptools.find_packages(),
      setup_requires=['setuptools_scm'],
      include_package_data=True,
      zip_safe=False)
