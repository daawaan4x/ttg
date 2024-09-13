from typing import List, Literal, Tuple
from dataclasses import dataclass
import re

left_paren_regex = r"(?P<left_paren>\()"
right_paren_regex = r"(?P<right_paren>\))"

not_regex = r"(?P<not>\bNOT\b|!|~)"
"Regex for NOT operators: `NOT`, `not`, `!`, `~`"

and_regex = r"(?P<and>\bAND\b|&|\^)"
"Regex for AND operators: `AND`, `and`, `&`, `^`"

or_regex = r"(?P<or>\bOR\b|\||v)"
"Regex for OR operators: `OR`, `or`, `|`, `v`"

then_regex = r"(?P<then>\bTHEN\b|>|->)"
"Regex for THEN operators: `THEN`, `then`, `>`, `->`"

variable_regex = r"(?P<variable>\b[A-Z]+\b)"
"Regex for variables - any combination of alphabet characters"

invalid_regex = r"(?P<invalid>[\S]+)"

combined_regex = "|".join(
    [
        left_paren_regex,
        right_paren_regex,
        not_regex,
        and_regex,
        or_regex,
        then_regex,
        variable_regex,
        invalid_regex,
    ]
)
"Combined Regex for iterating tokens"

TokenType = Literal[
    "left_paren", "right_paren", "not", "and", "or", "then", "variable", "invalid"
]


@dataclass
class Token:
    "Output data of the lexer after tokenization"

    type: TokenType
    "The classification of the value of the token"

    value: str
    "The matching input value of the token in its original input"

    span: Tuple[int, int]
    "The position range of the token in its original input"

    def __str__(self) -> str:
        return self.value


def tokenize(formula: str) -> List[Token]:
    "Turns the input formula into a sequence of tokens"

    # iterate for regex matches on input
    query = re.finditer(combined_regex, formula, re.IGNORECASE)

    # filter empty matches
    matches = filter(lambda match: match.group(), query)

    tokens = map(
        lambda match: Token(
            type=match.lastgroup, value=match.group(), span=match.span()
        ),
        matches,
    )

    return list(tokens)
