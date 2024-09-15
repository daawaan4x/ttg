from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from ttg.core.parser import BinaryExpr, Expr, UnaryExpr, VariableExpr

if TYPE_CHECKING:
    from ttg.core.lexer import Token

TruthTable = Dict[str, List[bool]]
"""
The Truth Table type stores a list of boolean values for each expression. This
represents the different outputs of the sub-expressions of the input formula
under all the possible set of truth values for all the variables.
"""

TruthValues = Dict[str, bool]
"""
The Truth Values type stores a boolean value for each expression. This represents
the outputs of the sub-expressions of the input formula under a single set of
truth values for all the variables.
"""


def truth_table_variables(variables: list[str]) -> list[TruthValues]:
    """Generate all truth value combinations for all the given variables.

    For convenience, instead of returning `TruthTable`, it returns a list of
    `TruthValues` which can be used directly in the Evaluator.
    """
    products: list[TruthValues] = []

    # Iterate all numbers from 0 to 2^n - 1 then use the individual bits in their
    # binary representation as the True & False values.
    count = len(variables)
    for binary in range(2**count):
        # The "not" below is solely for display purposes to generate the `True`
        # values first so that they appear first at the top in the table
        row = [not bool((binary >> bit) & 1) for bit in range(count)]
        product = dict(zip(variables, row))
        products.append(product)

    return products


class Evaluator:
    """Interpreter for the Syntax Tree of a Formula.

    A recursive interpreter implementation for traversing the
    Expression Tree of a propositional logic formula and
    calculating the individual result of each node at every level.
    """

    values: TruthValues

    def eval(self, expr: Expr) -> bool:  # noqa: D102
        if isinstance(expr, VariableExpr):
            return self.eval_variable(expr)
        if isinstance(expr, UnaryExpr):
            return self.eval_unary(expr)
        if isinstance(expr, BinaryExpr):
            return self.eval_binary(expr)
        return False

    def eval_variable(self, expr: VariableExpr) -> bool:  # noqa: D102
        return bool(self.values.get(expr.name.value))

    def eval_unary(self, expr: UnaryExpr) -> bool:  # noqa: D102
        value = self.eval(expr.right)
        if expr.operator.type == "not":
            value = not value
        self.values[str(expr)] = value  # save result for each expression
        return value

    def eval_binary(self, expr: BinaryExpr) -> bool:  # noqa: D102
        left, right = self.eval(expr.left), self.eval(expr.right)
        value = False
        if expr.operator.type == "and":
            value = left and right
        if expr.operator.type == "or":
            value = left or right
        if expr.operator.type == "then":
            value = (not left) or right
        self.values[str(expr)] = value  # save result for each expression
        return value

    def evaluate(self, tree: Expr, values: TruthValues) -> TruthValues:
        """Evaluate & Store the sub-expressions of a formula.

        Given the root node of an expression tree and the truth values for all
        the variables in the expression tree, it returns an extended set of
        truth values including the results of the sub-expressions of the
        propositional logic formula.
        """
        self.values = dict(values)
        self.eval(tree)
        return dict(self.values)


def evaluate(tokens: list[Token], tree: Expr) -> TruthTable:
    # wrapper function for convenience

    # filter & get variable names from list of tokens
    variables = [x.value for x in filter(lambda x: x.type == "variable", tokens)]

    table: TruthTable = {}
    evaluator = Evaluator()

    # for each truth values combination of the variables, evaluate the
    # expression tree and aggregate the result into a truth table
    for truth_values in truth_table_variables(variables):
        values = evaluator.evaluate(tree, truth_values)
        for key, value in values.items():
            table.setdefault(key, []).append(value)

    return table
