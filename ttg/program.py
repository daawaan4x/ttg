from __future__ import annotations

import sys

from rich.highlighter import Highlighter
from rich.pretty import Pretty
from rich.text import Text

from ttg.console import rich_console, rich_console_error
from ttg.core.evaluator import evaluate
from ttg.core.lexer import Token, tokenize
from ttg.core.parser import ParserError, parse
from ttg.formatter import format_truth_table


def program(formula: str, inspect: bool) -> None:
    """Central function for the program's logic."""
    if inspect:
        rich_console.print()
        rich_console.print("Comand-Line Arguments (sys.argv): ", end="")
        rich_console.print(sys.argv)

    try:
        if inspect:
            rich_console.print()
            rich_console.rule(formula)
            rich_console.print()
            rich_console.print({"input_length": len(formula)})

        tokens = tokenize(formula)
        if inspect:
            rich_console.print()
            rich_console.print({"token_count": len(tokens)})
            rich_console.print(tokens)
        validate_tokens(formula, tokens)

        try:
            tree = parse(tokens)
        except ParserError as exc:
            display_error(formula, [exc.token], exc.message)
            raise
        if inspect:
            rich_console.print()
            rich_console.print({"expression": str(tree)})
            rich_console.print(tree)

        truth_table = evaluate(tokens, tree)

        rich_table = format_truth_table(truth_table, title=formula)
        rich_console.print()
        rich_console.print(rich_table)
    except Exception as exc:
        rich_console_error.print()
        if inspect:
            rich_console_error.print_exception(show_locals=True)
        else:
            rich_console_error.print("Exception caught: ", style="bold red", end="")
            rich_console_error.print(Pretty(exc))


class TokenHighlighter(Highlighter):
    """Helper class for highlighting the positions of the tokens using `rich`."""

    tokens: list[Token]
    offset: int

    def __init__(self, tokens: list[Token], offset: int) -> None:  # noqa: D107
        super().__init__()
        self.tokens = tokens
        self.offset = offset

    def highlight(self, text: Text) -> None:  # noqa: D102
        for token in self.tokens:
            text.stylize(
                "underline bold red",
                token.span[0] + self.offset,
                token.span[1] + self.offset,
            )


def display_error(formula: str, invalid_tokens: list[Token], message: str) -> None:
    """Display error and highlight invalid or suspected tokens."""
    highlighter = TokenHighlighter(invalid_tokens, 1)
    rich_console.print()
    rich_console.print(message, end=": ")

    text = Text(f"'{formula}'")
    text.stylize("green")
    text = highlighter(text)
    rich_console.print(text)


def validate_tokens(formula: str, tokens: list[Token]) -> None:
    """Check invalid tokens and print the error."""
    invalid_tokens = list(filter(lambda x: x.type == "invalid", tokens))

    # skip funciton if no invalid tokens
    if len(invalid_tokens) == 0:
        return

    display_error(formula, invalid_tokens, "Invalid Token(s) Found")
    raise Exception("Invalid Token(s) Found", formula)
