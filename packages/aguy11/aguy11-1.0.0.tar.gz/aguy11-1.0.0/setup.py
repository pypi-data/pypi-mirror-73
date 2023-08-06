import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name = "aguy11",
  version = "1.0.0",
  description = "Module for finding cool and useful stuff quickly",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = "aguy11",
  author_email = "aguy11@guerrillamail.org",
  license = "MIT License",
  packages=setuptools.find_packages(),
  classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
],
  zip_safe=True,
  python_requires = ">=3.0",
)