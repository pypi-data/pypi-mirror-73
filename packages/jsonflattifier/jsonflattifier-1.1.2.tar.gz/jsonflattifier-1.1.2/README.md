# jsonflattifier

Converts a JSON Document with nested objects and their parameters to the JSON Document with Flat Denormalised Data.


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
> jsonflattifier flattify "{...}" --json --jsonpath-keys --no-table
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
> jsonflattifier flattify "{...}" --csv --no-table
```

```csv
['name'],['has']
John,apple
John,peach
```

**Print Table**

```shell
> jsonflattifier flattify "{...}"
```

| ['name'] | ['has'] |
| -------- | ------- |
| John     | apple   |
| John     | peach   |

2 rows in set


**More Examples**

https://gitlab.com/v.grigoryevskiy/json-flattifier/-/tree/master/tests/data

