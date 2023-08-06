# jsonflattifier

Converts a JSON Document with nested objects and their parameters to the JSON Document with Flat Denormalised Data.

**Installation**

```shell
> pip install jsonflattifier
```

**Input**

```json
{
  "name": "John",
  "has": [
    "apple",
    "peach"
  ]
}
```

**Get flat JSON**

```shell
> python3 -m jsonflattifier flattify "{\"name\":\"John\",\"has\":[\"apple\",\"peach\"]}" --json --jsonpath-keys --no-table
```

```json
[
  {
    "$['name']": "John",
    "$['has'][0]": "apple"
  },
  {
    "$['name']": "John",
    "$['has'][1]": "peach"
  }
]
```

**Get CSV**

```shell
> python3 -m jsonflattifier flattify "{\"name\":\"John\",\"has\":[\"apple\",\"peach\"]}" --csv --no-table
```

```csv
['name'],['has']
John,apple
John,peach
```

**Print Table**

```shell
> python3 -m jsonflattifier flattify "{\"name\":\"John\",\"has\":[\"apple\",\"peach\"]}"
```

| ['name'] | ['has'] |
| -------- | ------- |
| John     | apple   |
| John     | peach   |

2 rows in set


**More Examples**

https://gitlab.com/v.grigoryevskiy/json-flattifier/-/tree/master/tests/data

