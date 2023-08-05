"""Converts JSON with nested objects and their parameters
to the JSON with Flat Denormalised Data.
https://gitlab.com/v.grigoryevskiy/json-flattifier/
https://pypi.python.org/pypi/jsonflattifier
"""

from jsonflattifier.apis import (
    flattify,
    flattifys,
    flatjson_to_csv,
    flatjson_to_transposed_list,
    flatjson_to_print,
)

__author__ = "Valentin Grigoryevskiy"
__license__ = "MIT"
__version__ = "1.1.1"
