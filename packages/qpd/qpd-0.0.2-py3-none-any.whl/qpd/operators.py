from typing import Any, List, Dict, Tuple

import pandas as pd

from qpd._dataframe import Column, DataFrame


class Operators(object):
    def __call__(self, func_name: str, *args: Any, **kwargs: Any) -> Any:
        return getattr(self, func_name)(*args, **kwargs)

    def to_df(self, obj: Any) -> DataFrame:
        if isinstance(obj, DataFrame):
            return obj
        if isinstance(obj, pd.DataFrame):
            return DataFrame(Column(v, k) for k, v in obj.to_dict("series").items())
        raise ValueError(f"{obj} is not supported")

    def to_col(self, value: Any, name: str = "") -> Column:
        return Column(value, name)

    def to_native(self, df: DataFrame) -> Any:
        return pd.DataFrame({k: v.native for k, v in df.items()})

    def rename(self, col: Column, name: str) -> Column:
        return col.rename(name)

    def extract_col(self, df: DataFrame, name: str) -> Column:
        return df[name]

    def assemble_df(self, *args: Any) -> DataFrame:
        return DataFrame(*args)

    def basic_unary_arithmetic_op(self, col: Column, op: str) -> Column:
        if op == "+":
            return col
        if op == "-":
            return Column(0 - col.native)
        raise NotImplementedError(f"{op} is not supported")

    def binary_arithmetic_op(self, col1: Column, col2: Column, op: str) -> Column:
        if op == "+":
            return Column(col1.native + col2.native)
        if op == "-":
            return Column(col1.native - col2.native)
        if op == "*":
            return Column(col1.native * col2.native)
        if op == "/":
            return Column(col1.native / col2.native)
        raise NotImplementedError(f"{op} is not supported")

    def comparison_op(self, col1: Column, col2: Column, op: str) -> Column:
        if op == "==":
            return Column(col1.native == col2.native)
        if op == "!=":
            return Column(col1.native != col2.native)
        if op == "<":
            return Column(col1.native < col2.native)
        if op == "<=":
            return Column(col1.native <= col2.native)
        if op == ">":
            return Column(col1.native > col2.native)
        if op == ">=":
            return Column(col1.native >= col2.native)
        raise NotImplementedError(f"{op} is not supported")

    def binary_logical_op(self, col1: Column, col2: Column, op: str) -> Column:
        if op == "and":
            return Column(col1.native & col2.native)
        if op == "or":
            return Column(col1.native | col2.native)
        raise NotImplementedError(f"{op} is not supported")

    def logical_not(self, col: Column) -> Column:
        return Column(~col.native)

    def filter_col(self, col: Column, cond: Column) -> Column:
        if cond.native is True:
            return col
        if cond.native is False:
            return Column(col.native[[]])
        return Column(col.native[cond.native])

    def filter_df(self, df: DataFrame, cond: Column) -> DataFrame:
        ndf = self.to_native(df)[cond.native]
        return self.to_df(ndf)

    def group_agg(
        self, df: DataFrame, keys: List[str], agg_map: Dict[str, Tuple[str, str]]
    ) -> DataFrame:
        ndf = self.to_native(df)
        agg_map = {k: (v[0], self._map_agg_function(v[1])) for k, v in agg_map.items()}
        res = ndf.groupby(keys).agg(**agg_map).reset_index(drop=True)
        return self.to_df(res)

    def _map_agg_function(self, func: str) -> str:
        func = func.lower()
        if func == "avg":
            func = "mean"
        return func
