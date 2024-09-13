from rich.console import Console

from ttg.core.lexer import tokenize
from ttg.core.parser import Parser
from ttg.core.evaluator import evaluate
from ttg.formatter import format

rich_console = Console()


def compile(formula: str, inspect: bool):
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

    tree = Parser().parse(tokens)
    if inspect:
        rich_console.print()
        rich_console.print({"expression": str(tree)})
        rich_console.print(tree)

    truth_table = evaluate(tree)

    rich_table = format(truth_table, title=formula)
    rich_console.print()
    rich_console.print(rich_table)
