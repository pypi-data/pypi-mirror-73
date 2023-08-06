from pytest import raises
from triad.utils.hash import to_uuid

from qpd._dataframe import Column, DataFrame, DataFrames


def test_column():
    obj = "xx"
    c = Column(obj)
    assert obj is c.native
    assert "" == c.name
    assert not c.has_name
    raises(AssertionError, lambda: c.assert_has_name())
    c2 = c.rename("x")
    assert obj is c2.native
    assert "x" == c2.name
    assert to_uuid(c) != to_uuid(c2)
    c2.assert_has_name()
    c3 = Column(obj, "x")
    assert to_uuid(c3) == to_uuid(c2)


def test_dataframe():
    c1 = Column(1, "a")
    c2 = Column(1, "b")
    d = DataFrame(c1, c2)
    assert ["a", "b"] == list(d.keys())
    c3 = Column(1, "c")
    d2 = DataFrame(d, c3)
    assert ["a", "b", "c"] == list(d2.keys())
    d3 = DataFrame(c1, c2, c3)
    d4 = DataFrame(c1, [c2, c3])
    assert to_uuid(d2) != to_uuid(d)
    assert to_uuid(d2) == to_uuid(d3)
    assert to_uuid(d2) == to_uuid(d4)
    raises(ValueError, lambda: DataFrame(1))


def test_dataframe_get():
    c1 = Column(1, "a")
    c2 = Column(1, "b")
    d = DataFrame(c1, c2)
    assert d["a"] is c1
    assert d["*"] is d
    d2 = d[["b", "a"]]
    assert isinstance(d2, DataFrame)
    assert ["b", "a"] == list(d2.keys())
    assert to_uuid(d) != to_uuid(d2)
    d3 = d[["*"]]
    assert to_uuid(d3) == to_uuid(d)
    raises(ValueError, lambda: DataFrame(c1, c1))
    with raises(KeyError):
        d["x"]
    with raises(KeyError):
        d[["a", "x"]]
    with raises(ValueError):
        d[["a", "*"]]


def test_dataframes():
    c1 = Column(1, "a")
    c2 = Column(1, "b")
    c3 = Column(1, "a")
    c4 = Column(1, "c")
    df1 = DataFrame(c1, c2)
    df2 = DataFrame(c3, c4)
    df3 = DataFrame(c4)
    dfs1 = DataFrames(a=df1, b=df3)
    assert dfs1["a"] is df1
    assert dfs1["b"] is df3
    dfs2 = DataFrames(dict(a=df1), b=df3)
    assert to_uuid(dfs1) == to_uuid(dfs2)
    with raises(ValueError):
        DataFrames(1)
    dfs3 = DataFrames(dfs2, c=df2)
    assert dfs3["a"] is df1
    assert dfs3["b"] is df3
    assert dfs3["c"] is df2
    assert to_uuid(dfs1) != to_uuid(dfs3)


def test_dataframes_get():
    def assert_eq(df1, df2):
        assert list(df1.keys()) == list(df2.keys())
        assert to_uuid(df1) == to_uuid(df2)

    c1 = Column(1, "a")
    c2 = Column(1, "b")
    c3 = Column(1, "a")
    c4 = Column(1, "c")
    df1 = DataFrame(c1, c2)
    df2 = DataFrame(c3, c4)
    df3 = DataFrame(c4)
    dfs1 = DataFrames(a=df1, b=df3)
    assert_eq(dfs1.get("*"), DataFrame(c1, c2, c4))
    assert_eq(dfs1.get(["*"]), DataFrame(c1, c2, c4))
    assert_eq(dfs1.get(["c", "b"]), DataFrame(c4, c2))
    assert_eq(dfs1.get("a.*"), DataFrame(c1, c2))
    assert dfs1.get("a") is c1
    assert dfs1.get("a.a") is c1
    dfs2 = DataFrames(a=df1, b=df2)
    raises(ValueError, lambda: dfs2.get("*"))
    raises(ValueError, lambda: dfs2.get(["*"]))
    assert_eq(dfs2.get("a.*"), DataFrame(c1, c2))
    assert_eq(dfs2.get("b.*"), DataFrame(c3, c4))
