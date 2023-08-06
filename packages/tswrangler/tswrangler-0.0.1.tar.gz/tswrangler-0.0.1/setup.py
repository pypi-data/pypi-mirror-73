import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tswrangler",
    version="0.0.1",
    author="Kristian Arve",
    author_email="kr.arve@gmail.com",
    description="A small package to help wrangling pandas time series dataframes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kris7ian/tswrangler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)