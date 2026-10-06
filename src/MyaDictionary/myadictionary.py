from collections.abc import Hashable, Iterable, Iterator
from typing import Generic, TypeVar, overload

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
T = TypeVar("T")

_MISSING = object()

class MyADictionary(Generic[K, V]):
    """A hash table with separate chaining, written without the built-in ``dict``.

    Keys must be hashable. Lookups, insertions and deletions are O(1) on
    average; the table starts with ``DEFAULT_CAPACITY`` buckets and doubles
    in size whenever the load factor exceeds ``LOAD_FACTOR``.

    Supported operations::

        d[key] = value      store a value
        d[key]              look up a value, KeyError if missing
        del d[key]          remove a key, KeyError if missing
        key in d            membership test
        len(d)              number of stored items
        for key in d        iterate over keys

    Differences from the built-in ``dict``: iteration order follows the
    internal buckets rather than insertion order, and ``keys()``,
    ``values()`` and ``items()`` return one-shot iterators, not views.

    Example::

        >>> d = MyADictionary([("a", 1), ("b", 2)])
        >>> d["a"]
        1
        >>> d.get("missing", 0)
        0
    """
    DEFAULT_CAPACITY = 16
    LOAD_FACTOR = 0.75

    def __init__(self, items: Iterable[tuple[K, V]] | None = None) -> None:
        """Create a dictionary, optionally filled from an iterable of ``(key, value)`` pairs.

        If a key appears more than once, the last value wins.
        """
        self._capacity = self.DEFAULT_CAPACITY
        self._size = 0
        self._buckets: list[list[tuple[K, V]]] = [[] for _ in range(self._capacity)]
        if items is not None:
            for key, value in items:
                self[key] = value

    def _hash(self, key: object) -> int:
        return hash(key) % self._capacity

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]

        for bucket in old_buckets:
            for key, value in bucket:
                self._buckets[self._hash(key)].append((key, value))

    def __setitem__(self, key: K, value: V) -> None:
        """Store ``value`` under ``key``, replacing any existing value."""
        bucket = self._buckets[self._hash(key)]

        for i, (k, _) in enumerate(bucket):
            if k is key or k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self._size += 1 

        if self._size / self._capacity > self.LOAD_FACTOR:
            self._resize()

    def __getitem__(self, key: K) -> V:
        """Return the value stored under ``key``.

        Raises:
            KeyError: if ``key`` is not present.
        """
        bucket = self._buckets[self._hash(key)]

        for k, v in bucket:
            if k is key or k == key:
                return v
        raise KeyError(key)

    def __delitem__(self, key: K) -> None:
        """Remove ``key`` and its value.

        Raises:
            KeyError: if ``key`` is not present.
        """
        bucket = self._buckets[self._hash(key)]

        for i, (k, _) in enumerate(bucket):
            if k is key or k == key:
                del bucket[i]
                self._size -= 1
                return

        raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        """Return ``True`` if ``key`` is present."""
        bucket = self._buckets[self._hash(key)]
        return any(k is key or k == key for k, _ in bucket)

    def __len__(self) -> int:
        """Return the number of stored items."""
        return self._size

    def __iter__(self) -> Iterator[K]:
        """Iterate over the keys."""
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def items(self) -> Iterator[tuple[K, V]]:
        """Iterate over ``(key, value)`` pairs."""
        for bucket in self._buckets:
            for key, value in bucket:
                yield (key, value)

    def keys(self) -> Iterator[K]:
        """Iterate over the keys."""
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def values(self) -> Iterator[V]:
        """Iterate over the values."""
        for bucket in self._buckets:
            for _, value in bucket:
                yield value

    def get(self, key: K, default: V | None = None) -> V | None:
        """Return the value for ``key``, or ``default`` if ``key`` is not present."""
        try:
            return self[key]
        except KeyError:
            return default

    @overload
    def pop(self, key: K) -> V: ...

    @overload
    def pop(self, key: K, default: T) -> V | T: ...

    def pop(self, key: K, default: object = _MISSING) -> object:
        """Remove ``key`` and return its value.

        If ``key`` is not present, return ``default`` when one is given,
        otherwise raise ``KeyError``.
        """
        try:
            value = self[key]
        except KeyError:
            if default is _MISSING:
                raise
            return default

        del self[key]
        return value

    def clear(self) -> None:
        """Remove all items and shrink the table back to its default capacity."""
        self._capacity = self.DEFAULT_CAPACITY
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def __repr__(self) -> str:
        """Return ``MyADictionary([(key, value), ...])``, which recreates the dictionary when evaluated."""
        items = ", ".join(f"({key!r}, {value!r})" for key, value in self.items())
        return f"MyADictionary([{items}])"

    