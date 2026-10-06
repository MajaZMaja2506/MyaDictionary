from collections.abc import Hashable, Iterable, Iterator
from typing import Generic, TypeVar, overload

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")
T = TypeVar("T")

_MISSING = object()

class MyADictionary(Generic[K, V]):
    def __init__(self, items: Iterable[tuple[K, V]] | None = None) -> None:
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
        bucket = self._buckets[self._hash(key)]

        for k, v in bucket:
            if k is key or k == key:
                return v
        raise KeyError(key)

    def __delitem__(self, key: K) -> None:
        bucket = self._buckets[self._hash(key)]

        for i, (k, _) in enumerate(bucket):
            if k is key or k == key:
                del bucket[i]
                self._size -= 1
                return

        raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        bucket = self._buckets[self._hash(key)]
        return any(k is key or k == key for k, _ in bucket)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[K]:
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def items(self) -> Iterator[tuple[K, V]]:
        for bucket in self._buckets:
            for key, value in bucket:
                yield (key, value)

    def keys(self) -> Iterator[K]:
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def values(self) -> Iterator[V]:
        for bucket in self._buckets:
            for _, value in bucket:
                yield value

    def get(self, key: K, default: V | None = None) -> V | None:
        try:
            return self[key]
        except KeyError:
            return default

    @overload
    def pop(self, key: K) -> V: ...

    @overload
    def pop(self, key: K, default: T) -> V | T: ...

    def pop(self, key: K, default: object = _MISSING) -> object:
        try:
            value = self[key]
        except KeyError:
            if default is _MISSING:
                raise
            return default

        del self[key]
        return value

    def clear(self) -> None:
        self._capacity = self.DEFAULT_CAPACITY
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def __repr__(self) -> str:
        items = ", ".join(f"({key!r}, {value!r})" for key, value in self.items())
        return f"MyADictionary([{items}])"

    