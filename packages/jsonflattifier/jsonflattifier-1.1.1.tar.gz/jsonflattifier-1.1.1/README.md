# json-flattifier

Converts JSON Document with nested objects and their parameters to the JSON Document with Flat Denormalised Data.


**In:**

```json
{
  "name": "John",
  "has": [
    "apple",
    "peach"
  ]
}
```

**Out JSON:**

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

**Out CSV:**

```shell
> jsonflattifier flattify "{...}" --csv --no-table
```

```csv
['name'],['has']
John,apple
John,peach
```

**Out Table:**

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

