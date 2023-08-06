import pandas as pd
from pytest import raises
from triad.utils.hash import to_uuid

from qpd._parser.sql import QPDSql
from qpd._parser.visitors import (AggregationVisitor, PreAggregationVisitor,
                                  StatementVisitor)
from qpd.operators import Operators
from qpd.workflow.workflow import QPDWorkflow, QPDWorkflowContext


def test_select_from():
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT * FROM a",
        [[0, 1], [2, 3]], ["a", "b"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT a.* FROM a",
        [[0, 1], [2, 3]], ["a", "b"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT a.b,a FROM a",
        [[1, 0], [3, 2]], ["b", "a"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT b AS Xx,a AS Yy FROM a",
        [[1, 0], [3, 2]], ["Xx", "Yy"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT x.b AS Xx,a AS Yy FROM a AS x",
        [[1, 0], [3, 2]], ["Xx", "Yy"]
    )
    # inline relation
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT Y.b, a FROM (a AS x) AS Y",
        [[1, 0], [3, 2]], ["b", "a"]
    )
    # inline select
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT * FROM (SELECT b AS bb, a AS aa FROM a) AS Y",
        [[1, 0], [3, 2]], ["bb", "aa"]
    )

    not_support("SELECT * FROM a,b")
    not_support("SELECT * FROM a JOIN b ON a.x=b.x")
    not_support("SELECT *+2 AS x FROM a")
    not_support("SELECT 2+* AS x FROM a")


def test_select_const():
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT *, 'x\\'' AS x FROM a",
        [[0, 1, "x'"], [2, 3, "x'"]], ["a", "b", "x"]
    )
    # TODO: make this work?
    # assert_eq(
    #    [[0, 1], [2, 3]], ["a", "b"],
    #    "SELECT 1 AS x FROM a",
    #    [[1]], ["x"]
    # )


def test_where():
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT * FROM a WHERE a==0",
        [[0, 1]], ["a", "b"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT * FROM a WHERE TRUE",
        [[0, 1], [2, 3]], ["a", "b"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT * FROM a WHERE FALSE",
        [], ["a", "b"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT * FROM a WHERE FALSE AND TRUE",
        [], ["a", "b"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT * FROM a WHERE FALSE OR a==0",
        [[0, 1]], ["a", "b"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT * FROM a WHERE a==0 OR b=3",
        [[0, 1], [2, 3]], ["a", "b"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["x", "y"],
        "SELECT a.* FROM a WHERE x==0",
        [[0, 1]], ["x", "y"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["x", "y"],
        "SELECT a.y, x FROM a WHERE x==0",
        [[1, 0]], ["y", "x"]
    )


def test_arithmetic():
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT a+1 AS x, b*2 AS y, a*b AS c FROM a",
        [[1, 2, 0], [3, 6, 6]], ["x", "y", "c"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT (a+1)*(b-2) AS x, b FROM a",
        [[-1, 1], [3, 3]], ["x", "b"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT a+3*b+4/2 AS x, b FROM a",
        [[5, 1], [13, 3]], ["x", "b"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT a+3*b+4/2 AS x, a+3*b+4/2 AS y FROM a",
        [[5, 5], [13, 13]], ["x", "y"]
    )
    assert_eq(
        [[0, 1], [2, 3]], ["a", "b"],
        "SELECT 1 AS c, * FROM a",
        [[1, 0, 1], [1, 2, 3]], ["c", "a", "b"]
    )


def test_comparison():
    not_support("SELECT a<=>1 FROM a")

    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        "SELECT a>1 AS x,a==0 AS y,a!=0 AS z FROM a",
        [[False, True, False], [True, False, True]], ["x", "y", "z"]
    )
    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        "SELECT a<3 AS x, a<=3 AS y, b>=2 AS z FROM a",
        [[True, True, False], [False, True, True]], ["x", "y", "z"]
    )


def test_logical_op():
    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        """SELECT a==0 AND b==2 AS x, ((a>0) OR b==1) AND a<2 AS y,
        a==0 OR b<>1 AS z FROM a""",
        [[False, True, True], [False, False, True]], ["x", "y", "z"]
    )
    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        "SELECT NOT(((a>0) OR b==1) AND a<2) AS y FROM a",
        [[False], [True]], ["y"]
    )


def test_pre_agg():
    def assert_eq(data, cols, sql, expected, expected_cols, expected_map, expected_by):
        df, v = _debug_run(sql, "querySpecification", PreAggregationVisitor,
                           a=pd.DataFrame(data, columns=cols))
        ec = ["_" + to_uuid(x).split("-")[-1] for x in expected_cols]
        assert set(ec) == set(list(df.columns))
        assert expected == df[ec].values.tolist()

        f = [(k, v[0], v[1]) for k, v in v._agg_funcs.items()]
        f.sort(key=lambda k: k[0])
        expected = list(expected_map)
        expected.sort(key=lambda k: k[0])
        assert list(expected) == f

        assert set(expected_by) == set(v._group_by)

    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        """SELECT a,SUM(a) AS sa FROM a GROUP BY a
        """,
        [[0], [3]], ["a"],
        [("a", "a", "first"), ("SUM ( a )", "a", "sum")],
        ["a"]
    )
    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        """SELECT a,SUM(b) AS s FROM a GROUP BY a
        """,
        [[1, 0], [2, 3]], ["b", "a"],
        [("a", "a", "first"), ("SUM ( b )", "b", "sum")],
        ["a"]
    )
    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        """SELECT a,b,SUM(b)+a AS s FROM a GROUP BY b
        """,
        [[0, 1], [3, 2]], ["a", "b"],
        [("a", "a", "first"), ("b", "b", "first"), ("SUM ( b )", "b", "sum")],
        ["b"]
    )
    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        """SELECT a,b,SUM(b)+a AS s FROM a GROUP BY a*b
        """,
        [[0, 1, 0], [3, 2, 6]], ["a", "b", "a * b"],
        [("a", "a", "first"), ("b", "b", "first"), ("SUM ( b )", "b", "sum")],
        ["a * b"]
    )
    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        """SELECT a,SUM(b)+SUM(a) AS s FROM a GROUP BY a
        """,
        [[1, 0], [2, 3]], ["b", "a"],
        [("a", "a", "first"), ("SUM ( a )", "a", "sum"), ("SUM ( b )", "b", "sum")],
        ["a"]
    )
    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        """SELECT a AS x,SUM(a+b) AS s FROM a GROUP BY a
        """,
        [[1, 0], [5, 3]], ["a + b", "a"],
        [("a", "a", "first"), ("SUM ( a + b )", "a + b", "sum")],
        ["a"]
    )
    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        """SELECT a,SUM(a+b) * SUM(a+ b) AS c FROM a GROUP BY a, a+b*b
        """,
        [[1, 0, 1], [5, 3, 7]], ["a + b", "a", "a + b * b"],
        [("a", "a", "first"), ("SUM ( a + b )", "a + b", "sum")],
        ["a", "a + b * b"]
    )
    assert_eq(
        [[0, 1], [3, 2]], ["a", "b"],
        """SELECT a,sin(SUM(a+b)) AS s,b+SUM(a+b) AS s2 FROM a GROUP BY a+b
        """,
        [[0, 1, 1], [3, 2, 5]], ["a", "b", "a + b"],
        [("a", "a", "first"), ("b", "b", "first"), ("SUM ( a + b )", "a + b", "sum")],
        ["a + b"]
    )


def test_agg_select():
    def assert_eq(data, cols, sql, expected, expected_cols):
        df, v = _debug_run(sql, "querySpecification", AggregationVisitor,
                           a=pd.DataFrame(data, columns=cols))
        assert expected_cols == list(df.columns)
        assert expected == df.values.tolist()

    assert_eq(
        [[0, 1], [0, 2], [3, 2]], ["a", "b"],
        """SELECT a,SUM(b) AS sa FROM a GROUP BY a
        """,
        [[0, 3], [3, 2]], ["a", "sa"]
    )
    assert_eq(
        [[0, 1], [0, 2], [3, 2]], ["a", "b"],
        """SELECT a AS x,SUM(b) AS sa FROM a GROUP BY a
        """,
        [[0, 3], [3, 2]], ["x", "sa"]
    )
    assert_eq(
        [[0, 1, 4], [0, 2, 5], [3, 2, 6]], ["a", "b", "c"],
        """SELECT a,SUM(b)+SUM(c) AS s, SUM(b*c) AS t FROM a GROUP BY a
        """,
        [[0, 12, 14], [3, 8, 12]], ["a", "s", "t"]
    )
    assert_eq(
        [[0, 1, 4], [0, 2, 5], [3, 2, 6]], ["a", "b", "c"],
        """SELECT a,SUM(b)+a AS s FROM a GROUP BY a
        """,
        [[0, 3], [3, 5]], ["a", "s"]
    )


def test_agg():
    assert_eq(
        [[0, 1], [0, 2], [3, 2]], ["a", "b"],
        """SELECT a,SUM(b) AS sa, MAX(b) AS m FROM a GROUP BY a
        """,
        [[0, 3, 2], [3, 2, 2]], ["a", "sa", "m"]
    )
    assert_eq(
        [[0, 1], [0, 2], [3, 2]], ["a", "b"],
        """SELECT a,MIN(b) AS sa, AVG(b) AS m FROM a GROUP BY a
        """,
        [[0, 1, 1.5], [3, 2, 2]], ["a", "sa", "m"]
    )
    assert_eq(
        [[0, 1], [0, 2], [3, 2]], ["a", "b"],
        """SELECT a,SUM(b*b) AS sa FROM a WHERE b=2 GROUP BY a
        """,
        [[0, 4], [3, 4]], ["a", "sa"]
    )


def assert_eq(data, cols, sql, expected, expected_cols):
    df = _run(sql, a=pd.DataFrame(data, columns=cols))
    assert expected_cols == list(df.columns)
    assert expected == df.values.tolist()


def not_support(sql):
    with raises(NotImplementedError):
        _run(sql, a=pd.DataFrame([[0, 1]], columns=["a", "b"]))


def _run(sql, **kwargs):
    return _debug_run(sql, "singleStatement", StatementVisitor, **kwargs)[0]


def _debug_run(sql, rule, visitor, **kwargs):
    sql = QPDSql(sql, rule)
    ctx = QPDWorkflowContext(Operators(), kwargs)
    wf = QPDWorkflow(ctx)
    v = visitor(sql, wf, wf.dfs[list(kwargs.keys())[0]], wf.dfs)
    wf.assemble_output(v.visit(sql.tree))
    wf.run()
    return ctx.result, v
