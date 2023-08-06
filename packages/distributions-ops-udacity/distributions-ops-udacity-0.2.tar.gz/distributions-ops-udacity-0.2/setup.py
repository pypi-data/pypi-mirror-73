from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='distributions-ops-udacity',
      version='0.2',
      description='Gaussian distributions',
      packages=['distributions'],
      zip_safe=False)
