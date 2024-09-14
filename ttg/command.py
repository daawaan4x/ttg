from pathlib import Path

from ttg.console import rich_console
from ttg.compile import compile


import click


@click.command("tgg")
@click.argument("input", required=True)
@click.option("-f", "--file", is_flag=True, help="Treats the input as a filepath.")
@click.option("-i", "--inspect", is_flag=True, help="Display debug data.")
def command(input: str, file: bool = False, inspect: bool = False):
    # Test if "formula" is actually a filepath
    if file:
        filepath = Path(input)

        try:
            if not filepath.exists():
                raise Exception(f"'{filepath.absolute()}' does not exist")
            if not filepath.is_file() or not filepath.name.endswith(".txt"):
                raise Exception("The provided input file is not a '.txt' file")
        except Exception as exc:
            rich_console.print()
            rich_console.print(f"{exc.__class__.__name__}: ", style="bold red", end="")
            rich_console.print(exc)
            exit(-1)

        formulas = filepath.read_text().splitlines()
    else:
        formulas = [input]

    for formula in formulas:
        compile(formula, inspect)
