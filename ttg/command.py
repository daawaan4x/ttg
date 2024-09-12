import io
from typing import Literal

import click

from rich import inspect, print
from rich.console import Console
from rich.panel import Panel

from ttg.core.lexer import tokenize
from ttg.core.parser import Parser
from ttg.core.evaluator import evaluate
from ttg.formatter import format


@click.command('tgg')
@click.argument('formula', required=True)
@click.option('--debug', type=click.Choice(['token', 'tree'], False), help="Display debug data")
def command(formula: str, debug: Literal["token", "tree"]):
    if debug:
        print({"input_length": len(formula)})

    tokens = tokenize(formula)
    if debug == "token":
        print({"token_count": len(tokens)})
        return print(tokens)

    tree = Parser().parse(tokens)
    if debug == "tree":
        print({"expression": str(tree)})
        return print(tree)

    truth_table = evaluate(tree)

    rich_table = format(truth_table)
    rich_console = Console()
    rich_console.print()
    rich_console.print(rich_table)
