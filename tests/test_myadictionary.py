import pytest

from MyaDictionary import MyADictionary

class SameHash:

    def __init__(self, name: str) -> None:
        self.name = name

    def __hash__(self) -> int:
        return 1

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SameHash) and self.name == other.name


def test_init():
    empty = MyADictionary()
    assert len(empty) == 0
    assert not empty

    d = MyADictionary([("a", 1), ("b", 2), ("a", 3)])
    assert len(d) == 2
    assert d["a"] == 3
    assert d["b"] == 2


def test_set_get_delete():
    d = MyADictionary()
    d["a"] = 1
    d["b"] = 2
    d["a"] = 10
    assert d["a"] == 10
    assert len(d) == 2

    del d["a"]
    assert "a" not in d
    assert "b" in d
    assert len(d) == 1


def test_missing_key_raises_keyerror_with_key():
    d = MyADictionary()
    with pytest.raises(KeyError) as exc:
        d["missing"]
    assert exc.value.args == ("missing",)

    with pytest.raises(KeyError):
        del d["missing"]

    with pytest.raises(KeyError):
        d.pop("missing")


def test_special_keys():
    d = MyADictionary()
    d[None] = None
    assert d[None] is None

    d[1] = "int"
    d[1.0] = "float"
    assert d[1] == "float"

    nan = float("nan")
    d[nan] = 1
    d[nan] = 2
    assert d[nan] == 2
    assert len(d) == 3

    with pytest.raises(TypeError):
        d[[1, 2]] = "unhashable"


def test_colliding_keys():
    a, b, c = SameHash("a"), SameHash("b"), SameHash("c")
    d = MyADictionary([(a, 1), (b, 2), (c, 3)])
    assert (d[a], d[b], d[c]) == (1, 2, 3)

    del d[b]
    assert b not in d
    assert (d[a], d[c]) == (1, 3)
    assert len(d) == 2


def test_resize():
    d = MyADictionary()
    for i in range(12):
        d[i] = i
    for i in range(12):
        d[i] = -i
    assert d._capacity == 16

    d[12] = 12
    assert d._capacity == 32

    for i in range(1000):
        d[i] = i * 2
    assert len(d) == 1000
    assert len(d._buckets) == d._capacity
    assert all(d[i] == i * 2 for i in range(1000))


def test_iteration():
    pairs = [("a", 1), ("b", 2), ("c", 3)]
    d = MyADictionary(pairs)
    assert sorted(d) == ["a", "b", "c"]
    assert sorted(d.keys()) == ["a", "b", "c"]
    assert sorted(d.values()) == [1, 2, 3]
    assert sorted(d.items()) == pairs


def test_get_and_pop():
    d = MyADictionary([("a", 1), ("b", 2)])
    assert d.get("a") == 1
    assert d.get("missing") is None
    assert d.get("missing", 0) == 0

    assert d.pop("a") == 1
    assert "a" not in d
    assert d.pop("b", "default") == 2
    assert d.pop("missing", "default") == "default"
    assert d.pop("missing", None) is None
    assert len(d) == 0


def test_clear():
    d = MyADictionary((i, i) for i in range(1000))
    d.clear()
    assert len(d) == 0
    assert list(d.items()) == []
    assert len(d._buckets) == d._capacity == MyADictionary.DEFAULT_CAPACITY

    d["a"] = 1
    assert d["a"] == 1


def test_repr_round_trips():
    assert repr(MyADictionary()) == "MyADictionary([])"

    d = MyADictionary([("a", 1), (2, "b"), (None, 3.5)])
    copy = eval(repr(d), {"MyADictionary": MyADictionary})
    assert len(copy) == len(d)
    assert all(copy[key] == value for key, value in d.items())
