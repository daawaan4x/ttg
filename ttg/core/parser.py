from dataclasses import dataclass
from typing import List
from ttg.core.lexer import Token, TokenType


class Expr:
    """
    The Expression class represents the individual nodes of the Abstract Syntax
    Tree (AST), the final output of the parser.
    """

    pass


@dataclass
class VariableExpr(Expr):
    name: Token

    def __str__(self) -> str:
        return str(self.name)


@dataclass
class UnaryExpr(Expr):
    operator: Token
    right: Expr

    def __str__(self) -> str:
        return f"{self.operator}{self.right}"


@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __str__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"


class Parser:
    """
    A Recursive-Descent Parser implementation for propositional logic formulas.
    The grammar is defined in the individual parsing functions of this class in
    a pseudo-BNF notation.
    """

    # region Expressions

    def expr_primary(self):
        """
        expr_primary =
            \| variable
            \| ( expr )
        """
        if self.match(["left_paren"]):
            expr = self.expr()
            if not self.check("right_paren"):
                self.error(self.peek(), "Expected ')'")
            self.next()
            return expr

        if self.match(["variable"]):
            return VariableExpr(self.prev())

        self.error(self.peek(), "Expected expression")

    def expr_not(self):
        """
        expr_not =
            \| expr_primary
            \| NOT expr_not
        """
        if self.match(["not"]):
            operator = self.prev()
            right = self.expr_not()
            return UnaryExpr(operator, right)

        return self.expr_primary()

    def expr_and(self):
        """
        expr_and =
            \| expr_not
            \| expr_and AND expr_not
        """
        expr = self.expr_not()

        while self.match(["and"]):
            operator = self.prev()
            right = self.expr_not()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def expr_or(self):
        """
        expr_or =
            \| expr_and
            \| expr_or OR expr_and
        """
        expr = self.expr_and()

        while self.match(["or"]):
            operator = self.prev()
            right = self.expr_and()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def expr_then(self):
        """
        expr_then =
            \| expr_or
            \| expr_then THEN expr_or
        """
        expr = self.expr_or()

        while self.match(["then"]):
            operator = self.prev()
            right = self.expr_or()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def expr(self):
        """
        expr = expr_then
        """
        return self.expr_then()

    # endregion

    # region Helpers

    def error(self, token: Token, message: str):
        "Helper method for raising exceptions"
        raise Exception(message, token)

    def match(self, types: List[TokenType]) -> bool:
        "Moves to the next token if current token matches any of specified token types"
        for type in types:
            if self.check(type):
                self.next()
                return True
        return False

    def check(self, type: TokenType) -> bool:
        "Check if current token matches specified token type"
        if self.isdone():
            return False
        return self.peek().type == type

    def peek(self) -> Token:
        "Peeks at current token"
        return self.tokens[self.current_index]

    def prev(self) -> Token:
        "Peeks at previous token"
        return self.tokens[self.current_index - 1]

    def next(self) -> Token:
        "Moves to the next token unless its done"
        if not self.isdone():
            self.current_index += 1
        return self.prev()

    def isdone(self) -> bool:
        "Checks if parser is already past last token"
        return self.current_index == len(self.tokens)

    # endregion

    def parse(self, tokens: List[Token]):
        "Parses a list of tokens to construct an AST then returns the root node"
        self.tokens = list(tokens)
        self.current_index = 0

        return self.expr()

    tokens: List[Token]
    current_index: int = 0


def parse(tokens: List[Token]):
    # wrapper function for convenience
    return Parser().parse(tokens)
