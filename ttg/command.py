from pathlib import Path

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
        if not filepath.exists():
            raise Exception("The specified filepath does not exist")
        if not filepath.is_file() or not filepath.name.endswith(".txt"):
            raise Exception("The provided input file is not a .txt file")
        formulas = filepath.read_text().splitlines()
    else:
        formulas = [input]

    for formula in formulas:
        compile(formula, inspect)
