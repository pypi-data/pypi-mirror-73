import pathlib
from setuptools import setup #this will allow us to create distributed files

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="get-age",
    version="1.0.0",
    description="Gives your current age",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/priya-mal/get-age",
    author="Priya_mal",
    author_email="mv.priyanka18@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["age"],   #from which we want to distribute the file
    include_package_data=True,
    install_requires=[],   #3rd party modules which are needed to run our package
    entry_points={
        "console_scripts": [
            "age=age.__main__:main",  #age is the short name for our package
        ]
    },
)