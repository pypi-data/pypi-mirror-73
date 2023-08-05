import pathlib

from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
VERSION = (HERE / "__init__.py").read_text()
REQs = [str(ir.req) for ir in parse_requirements("requirements.txt", session='upload')]


# This call to setup() does all the work
setup(
    name="pipi_rest",
    version=VERSION,
    description="REST supported",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/eronrunner/pipi_rest",
    author="Eron",
    author_email="eron.runner@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("test",)),
    include_package_data=True,
    install_requires=REQs,
    entry_points={},
)