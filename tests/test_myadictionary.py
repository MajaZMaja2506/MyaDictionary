import pytest

from MyaDictionary import MyADictionary


class SameHash:
    """Key whose instances all land in the same bucket."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __hash__(self) -> int:
        return 1

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SameHash) and self.name == other.name


def test_empty():
    d = MyADictionary()
    assert len(d) == 0
    assert not d
    assert list(d) == []


def test_init_from_pairs():
    d = MyADictionary([("a", 1), ("b", 2)])
    assert len(d) == 2
    assert d["a"] == 1
    assert d["b"] == 2


def test_init_duplicate_keys_keeps_last():
    d = MyADictionary([("a", 1), ("a", 2)])
    assert len(d) == 1
    assert d["a"] == 2


def test_setitem_and_getitem():
    d = MyADictionary()
    d["a"] = 1
    assert d["a"] == 1
    assert len(d) == 1


def test_setitem_overwrites():
    d = MyADictionary()
    d["a"] = 1
    d["a"] = 2
    assert d["a"] == 2
    assert len(d) == 1


def test_getitem_missing_raises_keyerror_with_key():
    d = MyADictionary()
    with pytest.raises(KeyError) as exc:
        d["missing"]
    assert exc.value.args == ("missing",)


def test_delitem():
    d = MyADictionary([("a", 1), ("b", 2)])
    del d["a"]
    assert "a" not in d
    assert "b" in d
    assert len(d) == 1


def test_delitem_missing_raises_keyerror_with_key():
    d = MyADictionary()
    with pytest.raises(KeyError) as exc:
        del d["missing"]
    assert exc.value.args == ("missing",)


def test_contains():
    d = MyADictionary([("a", 1)])
    assert "a" in d
    assert "b" not in d
    assert 1 not in d


def test_none_as_key_and_value():
    d = MyADictionary()
    d[None] = None
    assert None in d
    assert d[None] is None
    assert len(d) == 1


def test_equal_keys_of_different_types_share_entry():
    d = MyADictionary()
    d[1] = "int"
    d[1.0] = "float"
    assert len(d) == 1
    assert d[1] == "float"


def test_unhashable_key_raises_typeerror():
    d = MyADictionary()
    with pytest.raises(TypeError):
        d[[1, 2]] = "x"


def test_nan_key_found_by_identity():
    nan = float("nan")
    d = MyADictionary()
    d[nan] = 1
    d[nan] = 2
    assert len(d) == 1
    assert nan in d
    assert d[nan] == 2


def test_colliding_keys():
    a, b, c = SameHash("a"), SameHash("b"), SameHash("c")
    d = MyADictionary([(a, 1), (b, 2), (c, 3)])
    assert len(d) == 3
    assert d[a] == 1
    assert d[b] == 2
    assert d[c] == 3

    del d[b]
    assert b not in d
    assert d[a] == 1
    assert d[c] == 3
    assert len(d) == 2


def test_resize_keeps_all_items():
    d = MyADictionary()
    for i in range(1000):
        d[i] = i * 2

    assert len(d) == 1000
    assert d._capacity > MyADictionary.DEFAULT_CAPACITY
    assert len(d._buckets) == d._capacity
    assert all(d[i] == i * 2 for i in range(1000))


def test_resize_happens_above_load_factor():
    d = MyADictionary()
    for i in range(12):
        d[i] = i
    assert d._capacity == 16

    d[12] = 12
    assert d._capacity == 32


def test_overwrite_does_not_resize():
    d = MyADictionary()
    for i in range(12):
        d[i] = i
    for i in range(12):
        d[i] = -i
    assert d._capacity == 16
    assert len(d) == 12


def test_iter_keys_values_items():
    pairs = [("a", 1), ("b", 2), ("c", 3)]
    d = MyADictionary(pairs)
    assert sorted(d) == ["a", "b", "c"]
    assert sorted(d.keys()) == ["a", "b", "c"]
    assert sorted(d.values()) == [1, 2, 3]
    assert sorted(d.items()) == pairs


def test_get():
    d = MyADictionary([("a", 1)])
    assert d.get("a") == 1
    assert d.get("missing") is None
    assert d.get("missing", 0) == 0


def test_pop_existing():
    d = MyADictionary([("a", 1), ("b", 2)])
    assert d.pop("a") == 1
    assert "a" not in d
    assert len(d) == 1


def test_pop_missing_raises_keyerror_with_key():
    d = MyADictionary()
    with pytest.raises(KeyError) as exc:
        d.pop("missing")
    assert exc.value.args == ("missing",)


def test_pop_missing_with_default():
    d = MyADictionary([("a", 1)])
    assert d.pop("missing", "default") == "default"
    assert d.pop("missing", None) is None
    assert len(d) == 1


def test_pop_existing_ignores_default():
    d = MyADictionary([("a", 1)])
    assert d.pop("a", "default") == 1
    assert len(d) == 0


def test_clear():
    d = MyADictionary()
    for i in range(1000):
        d[i] = i

    d.clear()
    assert len(d) == 0
    assert list(d.items()) == []
    assert d._capacity == MyADictionary.DEFAULT_CAPACITY
    assert len(d._buckets) == MyADictionary.DEFAULT_CAPACITY

    d["a"] = 1
    assert d["a"] == 1


def test_repr():
    assert repr(MyADictionary()) == "MyADictionary([])"
    assert repr(MyADictionary([("a", 1)])) == "MyADictionary([('a', 1)])"


def test_repr_round_trips():
    d = MyADictionary([("a", 1), (2, "b"), (None, 3.5)])
    copy = eval(repr(d), {"MyADictionary": MyADictionary})
    assert len(copy) == len(d)
    assert all(copy[key] == value for key, value in d.items())
