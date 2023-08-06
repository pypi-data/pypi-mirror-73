import itertools
import json
import re
from json import JSONDecodeError
from typing import List, Union, Type

from terminaltables import AsciiTable

NORMALISED_PATH_INDICATORS_REGEX = r"\$|\[\d\]"


# TODO: Unit Tests
def __flattify_runner(json_data, normalised_path: bool = False):
    prefix = "$" if normalised_path else ""
    denormalised_data = []

    if isinstance(json_data, list):
        for js in json_data:
            denormalised_data.extend(__denormalise(js, prefix, normalised_path))
    else:
        denormalised_data = __denormalise(json_data, prefix, normalised_path)

    json_result = json.dumps(denormalised_data, indent=2)
    return json_result


# TODO: Unit Tests
def __denormalise(data: dict, prefix: str, show_indices: bool) -> list:
    result = []
    intermediate_result = []

    for key, value in data.items():
        parent_prefix = f"{prefix}['{key}']"

        if isinstance(value, (str, int, float, bool)):
            __process_data(value, parent_prefix, intermediate_result)

        elif isinstance(value, dict):
            s = __denormalise(value, parent_prefix, show_indices)
            if s.__len__() == 1:
                intermediate_result.append([s])
            else:
                intermediate_result.append(s)

        elif isinstance(value, list):
            local_intermediate_result = []

            for index, val in enumerate(value):
                x_index_value = f"[{index}]" if show_indices else ""
                parent_prefix_with_index = parent_prefix + x_index_value

                if isinstance(val, str):
                    __process_data(
                        val, parent_prefix_with_index, local_intermediate_result
                    )

                elif isinstance(val, list):
                    for v in val:
                        s = __denormalise(v, parent_prefix_with_index, show_indices)
                        local_intermediate_result.append(s)

                else:
                    s = __denormalise(val, parent_prefix_with_index, show_indices)
                    for i in s:
                        local_intermediate_result.append(i)
            intermediate_result.append(local_intermediate_result)

    __cartesian_product(intermediate_result, result)

    return result


# TODO: Unit Tests
def __process_data(value, prefix: str, result: list) -> None:
    s = {prefix: str(value)}
    result.append([s])


# TODO: Unit Tests
def __cartesian_product(input: list, output: list) -> None:
    product = itertools.product(*input)
    for p in product:
        if isinstance(p, tuple):

            output.append(__tuple_to_dict(p))
        else:

            output.append(p)


# TODO: Unit Tests
def __tuple_to_dict(tup: tuple) -> dict:
    result = {}
    for t in tup:
        if isinstance(t, tuple):
            result.update(__tuple_to_dict(t))
        elif isinstance(t, list):
            for i in t:
                result.update(i)
        else:
            result.update(t)
    return result


# TODO: Unit Tests
def __transpose_json(json_object) -> List:
    header = []
    table_content = []
    table_data = []

    [
        [
            header.append(re.sub(NORMALISED_PATH_INDICATORS_REGEX, "", key))
            for key in js
            if re.sub(NORMALISED_PATH_INDICATORS_REGEX, "", key) not in header
        ]
        for js in json_object
    ]
    [table_content.extend(__compose_table_content(header, js)) for js in json_object]

    table_data.append(header)
    table_data.extend(table_content)

    return table_data


# TODO: Unit Tests
def __compose_table_content(header, json_object_item):
    result = []
    table_content = []
    table_content_item = []

    for h in header:
        r = 0
        for key, value in json_object_item.items():
            if h == re.sub(NORMALISED_PATH_INDICATORS_REGEX, "", key):
                table_content_item.append(value)
                r = 1
        if r == 0:
            table_content_item.append("")
    table_content.append(table_content_item)

    [result.append(i) for i in table_content]

    return result


# TODO: Unit Tests
def __print_table(data: list) -> None:
    table_instance = AsciiTable(data)
    print(table_instance.table)
    # TODO: 'row'/'rows' based on number of rows
    print(f"{len(data) - 1} rows in set")
    print()


# TODO: Unit Tests
def __print_json(json_object) -> None:
    __print_table(__transpose_json(json_object))


# TODO: Unit Tests
def __load_json_string(s: str) -> Union[Type[JSONDecodeError], str]:
    try:
        json_data = json.loads(s)
    except json.JSONDecodeError:
        return json.JSONDecodeError
    return json_data


# TODO: Unit Tests
def __load_json_file(path: str) -> Union[Type[JSONDecodeError], str]:
    try:
        with open(path, "r") as json_file:
            json_data = json.load(json_file)

    except json.JSONDecodeError:
        return json.JSONDecodeError
    return json_data
