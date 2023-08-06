from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='flightcontrol',
      version='0.2.0',
      description='Flight tracking resources',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/TimHanewich/FlightControl',
      author='Tim Hanewich',
      author_email='tahanewich@live.com',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False)