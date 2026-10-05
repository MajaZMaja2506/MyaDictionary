# MyaDictionary
Implementation of a dictionary in Python

A hash table with separate chaining, written without the built-in `dict`.

## Installation

```bash
pip install MyaDictionary
```

## Usage

The package is `MyaDictionary` and the class inside it is `MyADictionary`
(capital A). The constructor takes an iterable of `(key, value)` pairs.

```python
from MyaDictionary import MyADictionary

d = MyADictionary([("a", 1), ("b", 2)])
d["c"] = 3
del d["a"]

print(d["b"])          # 2
print("a" in d)        # False
print(len(d))          # 2
print(d.get("x", 0))   # 0
print(d.pop("c"))      # 3

for key, value in d.items():
    print(key, value)
```

## Development

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```
