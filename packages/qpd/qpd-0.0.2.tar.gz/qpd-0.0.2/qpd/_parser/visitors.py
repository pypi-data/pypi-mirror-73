from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Set, Tuple, Type, Union

from antlr4.tree.Tree import Token, Tree
from triad.utils.assertion import assert_or_throw
from triad.utils.hash import to_uuid

from _qpd_antlr import QPDParser as qp
from _qpd_antlr import QPDVisitor
from qpd._dataframe import Column, DataFrame, DataFrames
from qpd._parser.sql import QPDSql, _to_tokens
from qpd.workflow.workflow import QPDWorkflow, WorkflowDataFrame

AGGREGATION_FUNCTIONS: Set[str] = {"count", "avg", "min", "max", "sum", "first"}


class VisitorBase(QPDVisitor):
    def __init__(
        self, sql: QPDSql, workflow: QPDWorkflow, current_df: DataFrame, dfs: DataFrames
    ):
        self._sql = sql
        self._workflow = workflow
        self._current = current_df
        self._dfs = dfs

    def copy(self, tp: Type) -> "VisitorBase":
        return tp(self._sql, self._workflow, self._current, self._dfs)

    @property
    def workflow(self) -> QPDWorkflow:
        return self._workflow

    @property
    def sql(self) -> QPDSql:
        return self._sql

    # @property
    # def current(self) -> DataFrame:
    #    return self._current

    @property
    def dfs(self) -> DataFrames:
        return self._dfs

    # def collectChildren(self, node: Tree, tp: Type) -> List[Any]:
    #     result: List[Any] = []
    #     n = node.getChildCount()
    #     for i in range(n):
    #         c = node.getChild(i)
    #         if isinstance(c, tp):
    #             result.append(c.accept(self))
    #     return result

    def to_str(self, node: Union[Tree, Token, None], delimit: str = " ") -> str:
        if isinstance(node, Token):
            tokens: Iterable[Token] = [node]
        else:
            tokens = _to_tokens(node)
        return delimit.join([self.sql.raw_code[t.start : t.stop + 1] for t in tokens])

    # def get_dict(self, ctx: Tree, *keys: Any) -> Dict[str, Any]:
    #     res: Dict[str, Any] = {}
    #     for k in keys:
    #         v = getattr(ctx, k)
    #         if v is not None:
    #             res[k] = self.visit(v)
    #     return res

    def not_support(self, msg: str) -> None:
        raise NotImplementedError(msg)

    def assert_none(self, *nodes: Any) -> None:
        for node in nodes:
            if isinstance(node, list):
                if len(node) > 0:
                    self.not_support(f"{node} is not empty")
            elif node is not None:
                expr = self.to_str(node)
                self.not_support(f"{expr}")

    def visitFunctionName(self, ctx: qp.FunctionNameContext) -> str:
        if ctx.qualifiedName() is None:
            self.not_support(self.to_str(ctx))
        return self.to_str(ctx.qualifiedName()).lower()


class FromVisitor(VisitorBase):
    def __init__(
        self, sql: QPDSql, workflow: QPDWorkflow, current_df: DataFrame, dfs: DataFrames
    ):
        super().__init__(sql, workflow, current_df, dfs)

    def visitFunctionName(self, ctx: qp.FunctionNameContext) -> str:
        if ctx.qualifiedName() is None:
            self.not_support(self.to_str(ctx))
        return self.to_str(ctx.qualifiedName()).lower()

    def visitTableAlias(self, ctx: qp.TableAliasContext) -> str:
        self.assert_none(ctx.identifierList())
        if ctx.strictIdentifier() is None:
            return ""
        return self.to_str(ctx.strictIdentifier(), "")

    def visitTableName(self, ctx: qp.TableNameContext) -> Tuple[DataFrame, str]:
        self.assert_none(ctx.sample())
        df_name = self.to_str(ctx.multipartIdentifier(), "")
        assert_or_throw(df_name in self.dfs, KeyError(f"{df_name} is not found"))
        alias = self.visitTableAlias(ctx.tableAlias())
        if alias == "":
            alias = df_name
        return self.dfs[df_name], alias

    def visitAliasedQuery(self, ctx: qp.AliasedQueryContext) -> Tuple[DataFrame, str]:
        self.assert_none(ctx.sample())
        alias = self.visitTableAlias(ctx.tableAlias())
        assert_or_throw(alias != "", "inline query must have an alias")
        return self.copy(StatementVisitor).visit(ctx.query()), alias

    def visitAliasedRelation(
        self, ctx: qp.AliasedRelationContext
    ) -> Tuple[DataFrame, str]:
        self.assert_none(ctx.sample())
        df, a = self.copy(FromVisitor).visit(ctx.relation())
        alias = self.visitTableAlias(ctx.tableAlias())
        return df, alias if alias != "" else a

    def visitRelation(self, ctx: qp.RelationContext) -> Tuple[DataFrame, str]:
        self.assert_none(ctx.joinRelation())
        res = self.visit(ctx.relationPrimary())
        if res is None:  # pragma: no cover
            self.not_support(f"{self.to_str(ctx.relationPrimary())} is not supported")
        return res

    def visitFromClause(self, ctx: qp.FromClauseContext) -> Tuple[DataFrame, str]:
        rel = ctx.relation()
        if len(rel) > 1:
            self.not_support(self.to_str(ctx) + " is not supported")
        self.assert_none(ctx.lateralView(), ctx.pivotClause())
        return self.visit(rel[0])


class ExpressionVisitor(VisitorBase):
    def __init__(
        self, sql: QPDSql, workflow: QPDWorkflow, current_df: DataFrame, dfs: DataFrames
    ):
        super().__init__(sql, workflow, current_df, dfs)

    def visitStar(self, ctx: qp.StarContext) -> List[Column]:
        name = self.to_str(ctx, "")
        return self.dfs.get_columns(name)

    def visitColumnReference(self, ctx: qp.ColumnReferenceContext) -> List[Column]:
        name = self.to_str(ctx, "")
        return self.dfs.get_columns(name)

    def visitDereference(self, ctx: qp.DereferenceContext) -> List[Column]:
        name = self.to_str(ctx, "")
        return self.dfs.get_columns(name)

    def visitConstantDefault(self, ctx: qp.ConstantDefaultContext) -> List[Column]:
        raw = self.to_str(ctx, "")
        if raw.lower() == "true":
            value = True
        elif raw.lower() == "false":
            value = False
        else:
            value = eval(raw)
        return [self.workflow.const_to_col(value)]

    def visitParenthesizedExpression(
        self, ctx: qp.ParenthesizedExpressionContext
    ) -> List[Column]:
        return self.visit(ctx.expression())

    def visitArithmeticBinary(  # type: ignore
        self, ctx: qp.ArithmeticBinaryContext
    ) -> List[Column]:
        op = self.to_str(ctx.operator)
        left, right = self._get_single_left_right(ctx)
        return [self.workflow.op_to_col("binary_arithmetic_op", left, right, op)]

    def visitLogicalNot(self, ctx: qp.LogicalNotContext) -> List[Column]:
        col = self._get_single_column(ctx.booleanExpression())
        return [self.workflow.op_to_col("logical_not", col)]

    def visitPredicated(self, ctx: qp.PredicatedContext) -> Iterable[Column]:
        self.assert_none(ctx.predicate())
        return self.visit(ctx.valueExpression())

    def visitComparison(self, ctx: qp.ComparisonContext) -> List[Column]:
        def to_op(o: qp.ComparisonOperatorContext):
            if o.EQ():
                return "=="
            if o.NEQ():
                return "!="
            if o.NEQJ():
                return "!="
            if o.LT():
                return "<"
            if o.LTE():
                return "<="
            if o.GT():
                return ">"
            if o.GTE():
                return ">="
            self.not_support("comparator " + self.to_str(o))

        op = to_op(ctx.comparisonOperator())
        left, right = self._get_single_left_right(ctx)
        return [self.workflow.op_to_col("comparison_op", left, right, op)]

    def visitLogicalBinary(self, ctx: qp.LogicalBinaryContext):
        op = self.to_str(ctx.operator).lower()
        left, right = self._get_single_left_right(ctx)
        return [self.workflow.op_to_col("binary_logical_op", left, right, op)]

    def visitNamedExpression(self, ctx: qp.NamedExpressionContext) -> Iterable[Column]:
        self.assert_none(ctx.identifierList())
        alias = ""
        if ctx.errorCapturingIdentifier() is not None:
            alias = self.to_str(ctx.errorCapturingIdentifier(), "")
        for col in self.visit(ctx.expression()):
            yield col if alias == "" else col.rename(alias)

    def visitNamedExpressionSeq(
        self, ctx: qp.NamedExpressionSeqContext
    ) -> Iterable[Column]:
        for ne in ctx.namedExpression():
            for r in self.visit(ne):
                yield r

    def _get_single_left_right(self, ctx: Any) -> Tuple[Any, Any]:
        left = self._get_single_column(ctx.left)
        right = self._get_single_column(ctx.right)
        return left, right

    def _get_single_column(self, ctx: Any) -> Column:
        c = list(self.visit(ctx))
        if len(c) > 1:
            self.not_support(self.to_str(ctx))
        return c[0]


class PreAggregationVisitor(VisitorBase):
    def __init__(
        self, sql: QPDSql, workflow: QPDWorkflow, current_df: DataFrame, dfs: DataFrames
    ):
        super().__init__(sql, workflow, current_df, dfs)
        self._in_agg = False
        self._internal_cols: Dict[str, Column] = OrderedDict()
        self._mentioned_cols: Set[str] = set()
        self._agg_funcs: Dict[str, Tuple[str, str]] = OrderedDict()
        self._group_by: List[str] = []

    def visitStar(self, ctx: qp.StarContext) -> None:
        if not self._in_agg:
            self.not_support(self.to_str(ctx, ""))

    def visitColumnReference(self, ctx: qp.ColumnReferenceContext) -> None:
        if not self._in_agg:
            name = self.to_str(ctx, "")
            # TODO: validate
            self._agg_funcs[name] = (name, "first")
            self._mentioned_cols.add(name)

    def visitDereference(self, ctx: qp.DereferenceContext) -> None:
        if not self._in_agg:
            self.not_support(self.to_str(ctx, ""))

    def visitFunctionCall(self, ctx: qp.FunctionCallContext) -> None:
        func = self.visit(ctx.functionName())
        is_agg = False
        if func in AGGREGATION_FUNCTIONS:
            assert_or_throw(not self._in_agg, SyntaxError("Agg in agg"))
            self._in_agg = True
            is_agg = True
        if func == "count":
            self.not_support("COUNT")
        for x in ctx.argument:
            self.visit(x)
        self._in_agg = False
        if is_agg:
            assert_or_throw(len(ctx.argument) == 1, SyntaxError("invalid arguments"))
            self._visit_internal(ctx.argument[0])
            key = self.to_str(ctx)
            expr = self.to_str(ctx.argument[0])
            self._agg_funcs[key] = (expr, func)

    def visitNamedExpression(self, ctx: qp.NamedExpressionContext) -> None:
        self.assert_none(ctx.identifierList())
        self.visit(ctx.expression())

    def visitAggregationClause(self, ctx: qp.AggregationClauseContext):
        for e in ctx.expression():
            self._visit_internal(e, is_group_by=True)

    def visitRegularQuerySpecification(
        self, ctx: qp.RegularQuerySpecificationContext
    ) -> DataFrame:
        self.visit(ctx.selectClause())
        self.visit(ctx.aggregationClause())
        cols: List[Column] = []
        names: Set[str] = set()
        for k, v in self._internal_cols.items():
            name = "_" + to_uuid(k).split("-")[-1]
            cols.append(v.rename(name))
            names.add(name)
        for c in self._mentioned_cols:
            name = "_" + to_uuid(c).split("-")[-1]
            if name not in names:
                cols.append(self._current[c].rename(name))
                names.add(name)
        return WorkflowDataFrame(*cols)

    def _visit_internal(self, ctx: Any, is_group_by: bool = False) -> None:
        expr = self.to_str(ctx)
        if expr not in self._internal_cols:
            v = self.copy(ExpressionVisitor)
            col = v._get_single_column(ctx)
            self._internal_cols[expr] = col
        if is_group_by:
            assert_or_throw(
                expr not in self._group_by,
                SyntaxError(f"{expr} is duplicated in group by"),
            )
            self._group_by.append(expr)


class AggregationVisitor(ExpressionVisitor):
    def __init__(
        self, sql: QPDSql, workflow: QPDWorkflow, current_df: DataFrame, dfs: DataFrames
    ):
        super().__init__(sql, workflow, current_df, dfs)
        self._pre_agg: PreAggregationVisitor = self.copy(PreAggregationVisitor)
        self._agg_df: Any = None

    def visitStar(self, ctx: qp.StarContext) -> List[Column]:
        raise NotImplementedError

    def visitColumnReference(self, ctx: qp.ColumnReferenceContext) -> List[Column]:
        return [self._get_col(self.to_str(ctx, ""))]

    def visitDereference(self, ctx: qp.DereferenceContext) -> List[Column]:
        raise NotImplementedError

    def visitFunctionCall(self, ctx: qp.FunctionCallContext) -> List[Column]:
        func = self.visit(ctx.functionName())
        if func in AGGREGATION_FUNCTIONS:
            return [self._get_col(self.to_str(ctx))]
        else:
            return super().visitFunctionCall(ctx)

    def visitNamedExpression(self, ctx: qp.NamedExpressionContext) -> Iterable[Column]:
        self.assert_none(ctx.identifierList())
        alias = ""
        if ctx.errorCapturingIdentifier() is not None:
            alias = self.to_str(ctx.errorCapturingIdentifier(), "")
        for col in self.visit(ctx.expression()):
            yield col if alias == "" else col.rename(alias)

    def visitSelectClause(self, ctx: qp.SelectClauseContext) -> DataFrame:
        return WorkflowDataFrame(*list(self.visit(ctx.namedExpressionSeq())))

    def visitRegularQuerySpecification(
        self, ctx: qp.RegularQuerySpecificationContext
    ) -> DataFrame:
        df = self._pre_agg.visit(ctx)
        gp_keys = [self._name(x) for x in self._pre_agg._group_by]
        gp_map = {
            self._name(k): (self._name(v[0]), v[1])
            for k, v in self._pre_agg._agg_funcs.items()
        }
        self._mention_map = {self._name(x): x for x in self._pre_agg._mentioned_cols}
        print(gp_keys)
        print(gp_map)
        print(self._pre_agg._agg_funcs)
        print(list(df.keys()))
        self._agg_df = self.workflow.op_to_df(
            list(gp_map.keys()), "group_agg", df, gp_keys, gp_map
        )
        return self.visit(ctx.selectClause())

    def _get_col(self, name: str) -> Column:
        col = self._agg_df[self._name(name)]
        if name in self._pre_agg._mentioned_cols:
            col = col.rename(name)
        return col

    def _name(self, name: str) -> str:
        return "_" + to_uuid(name).split("-")[-1]


class StatementVisitor(VisitorBase):
    def __init__(
        self, sql: QPDSql, workflow: QPDWorkflow, current_df: DataFrame, dfs: DataFrames
    ):
        super().__init__(sql, workflow, current_df, dfs)

    def visitSelectClause(self, ctx: qp.SelectClauseContext) -> DataFrame:
        visitor = self.copy(ExpressionVisitor)
        return WorkflowDataFrame(*list(visitor.visit(ctx.namedExpressionSeq())))

    def visitWhereClause(self, ctx: qp.WhereClauseContext) -> DataFrame:
        visitor = self.copy(ExpressionVisitor)
        cond = visitor._get_single_column(ctx.booleanExpression())
        cols: List[Column] = []
        for name, col in self._current.items():
            col = self.workflow.op_to_col("filter_col", col, cond)
            cols.append(col.rename(name))
        return WorkflowDataFrame(*cols)

    def visitRegularQuerySpecification(
        self, ctx: qp.RegularQuerySpecificationContext
    ) -> DataFrame:
        self.assert_none(
            ctx.lateralView(), ctx.windowClause(),
        )
        from_visistor = self.copy(FromVisitor)
        df, name = from_visistor.visit(ctx.fromClause())
        if ctx.whereClause() is not None:
            v = StatementVisitor(self.sql, self.workflow, df, DataFrames({name: df}))
            df = v.visit(ctx.whereClause())
        if ctx.aggregationClause() is None:
            v = StatementVisitor(self.sql, self.workflow, df, DataFrames({name: df}))
            return v.visit(ctx.selectClause())
        else:
            agg = AggregationVisitor(
                self.sql, self.workflow, df, DataFrames({name: df})
            )
            return agg.visit(ctx)

    def visitQuery(self, ctx: qp.QueryContext) -> DataFrame:
        self.assert_none(ctx.ctes())
        return self.visit(ctx.queryTerm())

    def visitSingleStatement(self, ctx: qp.SingleStatementContext):
        return self.visit(ctx.statement())
