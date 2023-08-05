from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='evalml',
    version='0.0.1',
    author='Feature Labs, Inc.',
    author_email='support@featurelabs.com',
    description='evalml',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://featuretools.com',
    packages=find_packages(),
    classifiers=[
         'Development Status :: 3 - Alpha',
         'Intended Audience :: Developers',
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
         'Programming Language :: Python :: 3.7',
         'Programming Language :: Python :: 3.8'
    ],
    python_requires='>=3.6, <4',
    license='BSD 3-clause'
)
