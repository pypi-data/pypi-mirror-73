import os
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(name='distribo',
      version='0.1.2',
      description='Statistical distributions',
      long_description=README,
      long_description_content_type='text/markdown',
      packages=['distribo'],
      author='Raaj Tilak Sarma',
      author_email='raajtilaksarma@gmail.com',
      url="https://github.com/raajtilaksarma/distribo",
      license="MIT",
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
      install_requires=["matplotlib"],
      zip_safe=False)
