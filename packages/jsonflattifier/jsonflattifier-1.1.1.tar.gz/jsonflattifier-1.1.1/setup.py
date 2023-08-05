import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jsonflattifier",
    version="1.1.1",
    author="Valentin Grigoryevskiy",
    author_email="v.grigoryevskiy@gmail.com",
    description="Converts a JSON Document with nested objects and their parameters "
    "to the JSON Document with Flat Denormalised Data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/v.grigoryevskiy/json-flattifier",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="json csv flat table convert denormalise combinations",
    project_urls={
        "Source": "https://gitlab.com/v.grigoryevskiy/json-flattifier",
        "Tracker": "https://gitlab.com/v.grigoryevskiy/json-flattifier/issues",
    },
)
