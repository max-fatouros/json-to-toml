# json-to-toml
Converts JSON to TOML format. Preserves ordering and adds indentation.

Converts the values from keys named "note" into comments, replaces null-types with comments.
### Example
<table>
<tr>
<th> JSON (input) </th>
<th> TOML (output) </th>
</tr>
<tr>
<td>

```json
"person":
{
  "Note": "this is a person",
  "age": 22,
  "income": null
}

```

</td>
<td>

```toml
# this is a person
[person]
age = 22
# income
```

</td>
</tr>
</table>

### How to run
Run `main.py`, choose one or more JSON file to convert using the file selector.
