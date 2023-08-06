from collections import defaultdict
from typing import Any, Dict, Iterable, List, Set, Union

from triad.collections import IndexedOrderedDict
from triad.utils.assertion import assert_or_throw
from triad.utils.hash import to_uuid


class Column(object):
    def __init__(self, data: Any, col: str = ""):
        self._col = col
        self._data = data

    def __uuid__(self) -> str:
        return to_uuid(self.name, id(self.native))

    @property
    def native(self) -> Any:
        return self._data

    @property
    def name(self) -> str:
        return self._col

    def rename(self, name) -> "Column":
        return Column(self.native, name)

    @property
    def has_name(self) -> bool:
        return self.name != ""

    def assert_has_name(self) -> None:
        assert_or_throw(self.has_name, "column does not have a name")


class DataFrame(IndexedOrderedDict[str, Column]):
    def __init__(self, *args: Any):
        super().__init__()

        def add(objs):
            for a in objs:
                if isinstance(a, Column):
                    a.assert_has_name()
                    assert_or_throw(
                        a.name not in self, ValueError(f"{a.name} already exists")
                    )
                    self[a.name] = a
                elif isinstance(a, DataFrame):
                    for v in a.values():
                        assert_or_throw(
                            v.name not in self, ValueError(f"{v.name} already exists")
                        )
                        self[v.name] = v
                elif isinstance(a, Iterable):
                    add(a)
                else:
                    raise ValueError(f"{a} is not valid")

        add(args)
        self.set_readonly()

    def __getitem__(self, key: Union[str, List[str]]) -> Union[Column, "DataFrame"]:
        if isinstance(key, str):
            if key != "*":
                return super().__getitem__(key)
            return self
        res: List[Column] = []
        for col in key:
            if col == "*":
                res += list(self.values())
            else:
                res.append(super().__getitem__(col))
        return DataFrame(res)


class DataFrames(IndexedOrderedDict[str, DataFrame]):
    def __init__(self, *args: Any, **kwargs: Any):  # noqa: C901
        super().__init__()
        for d in args:
            if isinstance(d, Dict):
                self._update(d)
            else:
                raise ValueError(f"{d} is not valid to initialize DataFrames")
        self._update(kwargs)
        self.set_readonly()
        self._col_to_df: Dict[str, Set[str]] = defaultdict(set)
        for k, v in self.items():
            for c in v.keys():
                self._col_to_df[c].add(k)
        self._has_overlap = any(len(v) > 1 for v in self._col_to_df.values())

    def get(self, expr: Union[str, List[str]]) -> Union[Column, "DataFrame"]:
        if isinstance(expr, str):
            return self._get_single_expr(expr)
        return DataFrame(*[self._get_single_expr(x) for x in expr])

    def get_columns(self, expr: Union[str, List[str]]) -> List[Column]:
        res = self.get(expr)
        if isinstance(res, Column):
            return [res]
        return list(res.values())

    def _get_single_expr(self, expr: str) -> Union[Column, "DataFrame"]:
        ee = expr.split(".", 1)
        if len(ee) == 1:
            df_name, col_name = "", expr
        else:
            df_name, col_name = ee[0], ee[1]
        if col_name == "*":
            if df_name != "":
                return self[df_name][col_name]
            else:
                assert_or_throw(
                    not self._has_overlap, ValueError("There is schema overlap")
                )
                return DataFrame(*list(self.values()))
        elif df_name == "":
            dfs = self._col_to_df[col_name]
            assert_or_throw(len(dfs) > 0, ValueError(f"{col_name} is not defined"))
            assert_or_throw(
                len(dfs) == 1, ValueError(f"{col_name} in these dataframes {dfs}")
            )
            return self[next(iter(dfs))][col_name]
        else:
            df = self[df_name]
            assert_or_throw(
                col_name in df, ValueError(f"{df_name} does not have {col_name}")
            )
            return df[col_name]

    def _update(self, dfs: Dict):
        for k, v in dfs.items():
            assert_or_throw(isinstance(k, str), ValueError(f"{k} is not string"))
            assert_or_throw(k != "", ValueError("key can't be empty"))
            assert_or_throw(
                isinstance(v, DataFrame), ValueError(f"{v} is not DataFrame")
            )
            self[k] = v
