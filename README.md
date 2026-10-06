# MyaDictionary
Implementation of a dictionary in Python

A hash table with separate chaining, written without the built-in `dict`.

## Requirements

- [Python](https://www.python.org/downloads/) 3.10 or newer. Check with `python3 --version`.
- [pip](https://pip.pypa.io/en/stable/getting-started/), Python's package installer. It ships with
  Python; check with `python3 -m pip --version`.

Installing into a [virtual environment](https://docs.python.org/3/library/venv.html) is recommended so
the package doesn't mix with your system Python.

For development you also need [git](https://git-scm.com/downloads) and
[pytest](https://docs.pytest.org/), which `pip install -e ".[dev]"` below installs for you.

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
