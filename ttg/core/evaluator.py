from typing import Dict, List

from ttg.core.lexer import Token
from ttg.core.parser import BinaryExpr, Expr, UnaryExpr, VariableExpr

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


def truth_table_variables(variables: List[str]):
    """
    Generates all the possible set of truth values for all the given variables.
    For convenience, instead of returning `TruthTable`, it returns `TruthValues`
    which can be used directly in the Evaluator.
    """
    products: List[TruthValues] = list()

    # Iterate all numbers from 0 to 2^n - 1 in their binary representation then
    # use the individual bits as the True & False values.
    count = len(variables)
    for i in range(2**count):
        # The "not" below is solely for display purposes to generate the `True`
        # values first so that they appear first at the top in the table
        row = [not bool((i >> bit) & 1) for bit in range(count)]
        product = dict(zip(variables, row))
        products.append(product)

    return products


class Evaluator:
    """
    A recursive interpreter implementation that simplifies traversing the AST
    and calculating the individual result of each node at every level.
    """

    values: TruthValues

    def eval(self, expr: Expr) -> bool:
        if isinstance(expr, VariableExpr):
            return self.eval_variable(expr)
        if isinstance(expr, UnaryExpr):
            return self.eval_unary(expr)
        if isinstance(expr, BinaryExpr):
            return self.eval_binary(expr)

    def eval_variable(self, expr: VariableExpr) -> bool:
        return bool(self.values.get(expr.name.value))

    def eval_unary(self, expr: UnaryExpr) -> bool:
        value = self.eval(expr.right)
        if expr.operator.type == "not":
            value = not value
        self.values[str(expr)] = value  # save result for each expression
        return value

    def eval_binary(self, expr: BinaryExpr) -> bool:
        left, right = self.eval(expr.left), self.eval(expr.right)
        if expr.operator.type == "and":
            value = left and right
        if expr.operator.type == "or":
            value = left or right
        if expr.operator.type == "then":
            value = (not left) or right
        self.values[str(expr)] = value  # save result for each expression
        return value

    def evaluate(self, expr: Expr, values: TruthValues) -> TruthValues:
        self.values = dict(values)
        self.eval(expr)
        return dict(self.values)


def evaluate(tokens: List[Token], tree: Expr) -> TruthTable:
    # filter & get variable names from list of tokens
    variables = list(
        map(lambda x: x.value, filter(lambda x: x.type == "variable", tokens))
    )

    table: TruthTable = dict()
    evaluator = Evaluator()

    # for each truth values combination of the variables, evaluate the
    # expression tree and aggregate the result into a truth table
    for truth_values in truth_table_variables(variables):
        values = evaluator.evaluate(tree, truth_values)
        for key, value in values.items():
            table.setdefault(key, list()).append(value)

    return table
