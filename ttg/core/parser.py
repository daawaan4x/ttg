from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ttg.core.lexer import Token, TokenType


class Expr:
    """Represents the individual nodes of the Expression Tree."""


@dataclass
class GroupExpr(Expr):  # noqa: D101
    child: Expr

    def __str__(self) -> str:  # noqa: D105
        return f"({self.child})"


@dataclass
class VariableExpr(Expr):  # noqa: D101
    name: Token

    def __str__(self) -> str:  # noqa: D105
        return str(self.name)


@dataclass
class UnaryExpr(Expr):  # noqa: D101
    operator: Token
    right: Expr

    def __str__(self) -> str:  # noqa: D105
        space = ""
        if self.operator.__str__().isalpha():  # in case operator is a word
            space = " "
        return f"{self.operator}{space}{self.right}"


@dataclass
class BinaryExpr(Expr):  # noqa: D101
    left: Expr
    operator: Token
    right: Expr

    def __str__(self) -> str:  # noqa: D105
        return f"{self.left} {self.operator} {self.right}"


@dataclass
class ParserError(Exception):  # noqa: D101
    message: str
    token: Token


class Parser:
    """Recursive-Descent Parser implementation for propositional logic formulas.

    The grammar is defined in the individual parsing functions of this class in
    a pseudo-BNF notation.
    """

    # region Expressions

    def expr_primary(self) -> GroupExpr | VariableExpr:
        """Parse primary expression.

        expr_primary =
            | ( expr )
            | variable
        """
        if self.match(["left_paren"]):
            expr = self.expr()
            if not self.check("right_paren"):
                raise ParserError("Expected ')'", self.peek())
            self.next()
            return GroupExpr(expr)

        if self.match(["variable"]):
            return VariableExpr(self.prev())

        raise ParserError("Expected variable", self.peek())

    def expr_not(self) -> Expr | VariableExpr | UnaryExpr:
        """Parse a NOT expression.

        expr_not =
            | NOT expr_not
            | expr_primary
        """
        if self.match(["not"]):
            operator = self.prev()
            right = self.expr_not()
            return UnaryExpr(operator, right)

        return self.expr_primary()

    def expr_and(self):  # noqa: ANN201
        """Parse an AND expression.

        expr_and =
            | expr_not AND expr_and
            | expr_not
        """
        expr = self.expr_not()

        while self.match(["and"]):
            operator = self.prev()
            right = self.expr_not()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def expr_or(self):  # noqa: ANN201
        """Parse an OR expression.

        expr_or =
            | expr_and OR expr_or
            | expr_and
        """
        expr = self.expr_and()

        while self.match(["or"]):
            operator = self.prev()
            right = self.expr_and()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def expr_then(self):  # noqa: ANN201
        """Parse a THEN expression.

        expr_then =
            | expr_or THEN expr_then
            | expr_or
        """
        expr = self.expr_or()

        while self.match(["then"]):
            operator = self.prev()
            right = self.expr_or()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def expr_only_if(self):  # noqa: ANN201
        """Parse a ONLY_IF expression.

        expr_only_if =
            | expr_then THEN expr_only_if
            | expr_then
        """
        expr = self.expr_then()

        while self.match(["only_if"]):
            operator = self.prev()
            right = self.expr_then()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def expr(self):  # noqa: ANN201
        """Parse any expression.

        expr = expr_only_if
        """
        return self.expr_only_if()

    # endregion

    # region Helpers

    def match(self, types: list[TokenType]) -> bool:
        """Move to the next if current token matches any of specified token types."""
        for t in types:
            if self.check(t):
                self.next()
                return True
        return False

    def check(self, type: TokenType) -> bool:
        """Check if current token matches specified token type."""
        if self.isdone():
            return False
        return self.peek().type == type

    def peek(self) -> Token:
        """Peek at current token. Returns previous if done."""
        if self.isdone():
            return self.prev()
        return self.tokens[self.current_index]

    def prev(self) -> Token:
        """Peek at previous token."""
        return self.tokens[self.current_index - 1]

    def next(self) -> Token:
        """Move to the next token unless its done."""
        if not self.isdone():
            self.current_index += 1
        return self.prev()

    def isdone(self) -> bool:
        """Check if parser is already past last token."""
        return self.current_index == len(self.tokens)

    # endregion

    def parse(self, tokens: list[Token]) -> Expr:
        """Parse a list of tokens to construct an AST then returns the root node."""
        self.tokens = list(tokens)
        self.current_index = 0

        tree = self.expr()
        if not self.isdone():
            raise ParserError("Expected end of formula", self.peek())

        return tree

    tokens: list[Token]
    current_index: int = 0


def parse(tokens: list[Token]) -> Expr:
    # wrapper function for convenience
    return Parser().parse(tokens)
