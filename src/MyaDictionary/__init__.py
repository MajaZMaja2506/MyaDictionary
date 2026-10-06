"""A dictionary implemented from scratch.

The package exports a single class, :class:`MyADictionary`, a generic hash
table with separate chaining that mirrors the behaviour of the built-in
``dict`` for the operations it supports.

Basic usage::

    >>> from MyaDictionary import MyADictionary
    >>> e = MyADictionary()
    >>> d = MyADictionary([("a", 1), ("b", 2)])
    >>> d["c"] = 3
    >>> d["a"]
    1
    >>> "b" in d
    True
    >>> len(d)
    3
    >>> d.pop("c")
    3
    >>> sorted(d.items())
    [('a', 1), ('b', 2)]

"""

from .myadictionary import MyADictionary

__all__ = ["MyADictionary"]
