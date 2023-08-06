from json import JSONDecodeError
from typing import List, Type, Union

from jsonflattifier.helpers import (
    __flattify_runner,
    __transpose_json,
    __print_json,
    __load_json_string,
    __load_json_file,
)


def flattify(
    path: str, normalised_path: bool = False
) -> Union[Type[JSONDecodeError], str]:
    """
    Converts a Tree Data (provided in the JSON File) to an Array of 'flat' denormalised Records,
    which can be represented in the classic Two-Dimensional Table, stored in the JSON Format.
    Example
          [x,y],[[A,a],[B,b]] =
        = (x+y)*((A+a)*(B+b)) =
        = (x+y)*(AB+Ab+aB+ab) =
        = xAB+xAb+xaB+xab+yAB+yAb+yaB+yab

    :param path: JSON Document as a Pointer to a File
    :param normalised_path: Use the jsonpath Normalised Path for Keys; False by default
    :return: JSON Document as a String with a List of denormalised Objects
    """

    json_data = __load_json_file(path)

    return __flattify_runner(json_data, normalised_path)


def flattifys(
    s: str, normalised_path: bool = False
) -> Union[Type[JSONDecodeError], str]:
    """
    Converts a Tree Data (provided in the JSON String) to an Array of 'flat' denormalised Records,
    which can be represented in the classic Two-Dimensional Table, stored in the JSON Format.
    Example
          [x,y],[[A,a],[B,b]] =
        = (x+y)*((A+a)*(B+b)) =
        = (x+y)*(AB+Ab+aB+ab) =
        = xAB+xAb+xaB+xab+yAB+yAb+yaB+yab

    :param s: JSON Document as a String
    :param normalised_path: Use the jsonpath Normalised Path for Keys; False by default
    :return: JSON Document with a List of denormalised Objects
    """

    json_data = __load_json_string(s)

    return __flattify_runner(json_data, normalised_path)


def flatjson_to_csv(json_string) -> Union[Type[JSONDecodeError], str]:
    """
    Turns Flat JSON into CSV:
        keys->columns
        values->cells
    Example
        flatjson_to_csv('{key1:value1,key2:value2}') --> key1,key2\r\nvalue1,value2

    :param json_string: JSON Document with a List of "flat" Objects (no Lists, no Nested Objects)
    :return: CSV Document as a String
    """

    json_data = __load_json_string(json_string)

    csv_list = "\n".join(
        ",".join(str(i) for i in row) for row in __transpose_json(json_data)
    )

    return csv_list


def flatjson_to_transposed_list(json_string) -> Union[Type[JSONDecodeError], List]:
    """
    Turns Flat JSON into List:
        keys->columns
        values->cells
    Example
        flatjson_to_csv('{key1:value1,key2:value2}') --> [(key1,key2),(value1,value2)]

    :param json_string: JSON Document with a List of "flat" Objects (no Lists, no Nested Objects)
    :return: A List of Rows: first for the Header with Keys and others for Values
    """

    json_data = __load_json_string(json_string)

    return __transpose_json(json_data)


def flatjson_to_print(json_string) -> Type[JSONDecodeError]:
    """
    Prints Flat JSON as a Table:
        keys->columns
        values->cells
    Example
        flatjson_to_csv('{key1:value1,key2:value2}') -->
        +--------+--------+
        | key1   | key2   |
        +--------+--------+
        | value1 | value2 |
        +--------+--------+

    :param json_string: JSON Document with a List of "flat" Objects (no Lists, no Nested Objects)
    :return: None
    """

    json_data = __load_json_string(json_string)

    __print_json(json_data)
