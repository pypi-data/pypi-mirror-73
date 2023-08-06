from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='distributions_exer',
    version='0.2',
    description='General, Gaussian, and Binomial distributions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['distributions_exer'],
    zip_safe=False
)
