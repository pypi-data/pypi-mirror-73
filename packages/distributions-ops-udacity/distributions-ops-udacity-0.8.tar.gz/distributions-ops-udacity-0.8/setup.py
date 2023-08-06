from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='distributions-ops-udacity',
      version='0.8',
      description='Gaussian distributions',
      long_description=long_description,
      packages=['distributions'],
      zip_safe=False)
