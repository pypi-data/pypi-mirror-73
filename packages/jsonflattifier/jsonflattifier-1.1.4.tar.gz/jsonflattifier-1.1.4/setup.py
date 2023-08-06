from setuptools import setup, find_packages

from jsonflattifier.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="jsonflattifier",
    version=__version__,
    author="Valentin Grigoryevskiy",
    author_email="v.grigoryevskiy@gmail.com",
    license="MIT",
    description="Converts a JSON Document with nested objects and their parameters "
    "to the JSON Document with Flat Denormalised Data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/v.grigoryevskiy/json-flattifier",
    packages=find_packages("jsonflattifier"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["terminaltables",],
    python_requires=">=3.6",
    keywords="json csv flat flattify flatten table convert denormalise combinations",
    project_urls={
        "Source": "https://gitlab.com/v.grigoryevskiy/json-flattifier",
        "Tracker": "https://gitlab.com/v.grigoryevskiy/json-flattifier/issues",
    },
)
