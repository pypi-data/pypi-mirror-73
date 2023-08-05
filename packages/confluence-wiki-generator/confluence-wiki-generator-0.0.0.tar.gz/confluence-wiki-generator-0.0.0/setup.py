import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="confluence-wiki-generator",
  varsion="0.0.1",
  author="Cuan Clifford",
  author_email="cliffordcuan@gmail.com",
  description="A Confluence Wiki markup generator",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/cjclifford/confluence-wiki-generator",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ],
  python_requires='>=3.8'
)