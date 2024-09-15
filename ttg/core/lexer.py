from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

left_paren_regex = r"(?P<left_paren>\()"
right_paren_regex = r"(?P<right_paren>\))"

not_regex = r"(?P<not>\bNOT\b|!|~|¬)"
"Regex for NOT operators: `NOT`, `not`, `!`, `~`, `¬`"

and_regex = r"(?P<and>\bAND\b|&&|&|\^|∧)"
"Regex for AND operators: `AND`, `and`, `&`, `&&`, `^`, `∧`"

or_regex = r"(?P<or>\bOR\b|\|\||\||v|∨)"  # noqa: RUF001
"Regex for OR operators: `OR`, `or`, `|`, `||`, `v`, `∨`"  # noqa: RUF001

then_regex = r"(?P<then>\bTHEN\b|>|->|→)"
"Regex for THEN operators: `THEN`, `then`, `>`, `->`, `→`"

variable_regex = r"(?P<variable>\b[A-Z]+\b)"
"Regex for variables - any combination of alphabet characters"

invalid_regex = r"(?P<invalid>[\S]+)"

combined_regex = "|".join(  # noqa: FLY002
    [
        left_paren_regex,
        right_paren_regex,
        not_regex,
        and_regex,
        or_regex,
        then_regex,
        variable_regex,
        invalid_regex,
    ],
)
"Combined Regex for iterating tokens"

TokenType = Literal[
    "left_paren",
    "right_paren",
    "not",
    "and",
    "or",
    "then",
    "variable",
    "invalid",
]


@dataclass
class Token:
    """Output data of the lexer after tokenizing the propositional logic formula."""

    type: TokenType
    "The classification of the value of the token"

    value: str
    "The matching input value of the token in its original input"

    span: tuple[int, int]
    "The position range of the token in its original input"

    def __str__(self) -> str:  # noqa: D105
        return self.value


def tokenize(formula: str) -> list[Token]:
    """Turn the input formula into a sequence of tokens.

    The tokenize function is resilient and will not raise errors for invalid tokens
    but will instead create a `Token(type="invalid")` added in the list.
    """
    formula += " "

    # iterate for regex matches on input
    query = re.finditer(combined_regex, formula, re.IGNORECASE)

    # filter empty matches
    matches = filter(lambda match: match.group(), query)

    # map regex matches to tokens
    tokens = (
        Token(type=match.lastgroup, value=match.group(), span=match.span())  # type: ignore reportArgumentType
        for match in matches
    )

    return list(tokens)
