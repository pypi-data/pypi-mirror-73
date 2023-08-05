import itertools
import json
import logging.config
import re
from typing import List

from terminaltables import AsciiTable

from config.config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("root")

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
    logger.debug("json_result" + str(json_result))
    return json_result


# TODO: Unit Tests
def __denormalise(data: dict, prefix: str, show_indices: bool) -> list:
    result = []
    intermediate_result = []

    for key, value in data.items():

        parent_prefix = prefix + "['" + str(key) + "']"

        if isinstance(value, (str, int, float, bool)):
            s = {parent_prefix: str(value)}
            intermediate_result.append([s])
            logger.debug("Appended to result:  " + str([s]))

        elif isinstance(value, dict):
            s = __denormalise(value, parent_prefix, show_indices)
            if s.__len__() == 1:
                intermediate_result.append([s])
                logger.debug("Appended to result:  " + str([s]))
            else:
                intermediate_result.append(s)
                logger.debug("Appended to result:  " + str(s))

        elif isinstance(value, list):
            x = 0
            x_index_value = ""
            local_intermediate_result = []

            for val in value:
                if show_indices is True:
                    x_index_value = "[" + str(x) + "]"
                parent_prefix_with_index = parent_prefix + x_index_value

                if isinstance(val, str):
                    s = {parent_prefix_with_index: str(val)}
                    local_intermediate_result.append([s])
                    logger.debug("Appended to local_result:  " + str([s]))
                elif isinstance(val, list):
                    logger.debug("Nested list: {val}".format(val=str(val)))
                    for v in val:
                        s = __denormalise(v, parent_prefix_with_index, show_indices)
                        for i in s:
                            local_intermediate_result.append(i)
                else:
                    logger.debug(
                        "List Element, which not srt or list: {val}".format(
                            val=str(val)
                        )
                    )
                    s = __denormalise(val, parent_prefix_with_index, show_indices)
                    for i in s:
                        local_intermediate_result.append(i)
                x += 1

            intermediate_result.append(local_intermediate_result)
            logger.debug("Appended to result:  " + str(local_intermediate_result))

        else:
            logger.debug(
                "null value: " + '"' + parent_prefix + '": ' + str(value) + "'"
            )

    product = itertools.product(*intermediate_result)
    for p in product:
        if isinstance(p, tuple):
            result.append(__tuple_to_dict(p))
        else:
            result.append(p)

    return result


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
    # def print_table(data=TABLE_DATA, title="TITLE") -> None:
    table_instance = AsciiTable(data)
    print(table_instance.table)
    # TODO: 'row'/'rows' based on number of rows
    print(f"{len(data) - 1} rows in set")
    print()


# TODO: Unit Tests
def __print_json(json_object) -> None:
    __print_table(__transpose_json(json_object))
