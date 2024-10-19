import sys
from pathlib import Path

import click

from ttg.console import rich_console
from ttg.program import program

hero = r"""
 ______   ______   ______   
/\__  _\ /\__  _\ /\  ___\  
\/_/\ \/ \/_/\ \/ \ \ \__ \ 
   \ \_\    \ \_\  \ \_____\
    \/_/     \/_/   \/_____/

"Truth Table Generator" by [bold]Theone Eclarin[/bold]
   [bright_black]... Press (Cmd/Ctrl + C) to force-exit ...[/bright_black] """  # noqa: W291


@click.command("tgg")
@click.argument("input", required=False)
@click.option("-f", "--file", is_flag=True, help="Treats the input as a filepath.")
@click.option("-i", "--inspect", is_flag=True, help="Display debug data.")
def command(input: str, file: bool = False, inspect: bool = False) -> None:
    # If input is a filepath, read formulas from file
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
            sys.exit(-1)

        formulas = filepath.read_text().splitlines()
        for formula in formulas:
            program(formula, inspect)

    # If input exists, assume its a formula and run program once
    elif input:
        program(input, inspect)

    # Else, run program in interactive mode
    else:
        rich_console.print(hero)

        while True:
            rich_console.print()
            formula = rich_console.input(
                "Enter a [bright_magenta italic]formula[/bright_magenta italic]: ",
            )
            program(formula, inspect)

            rich_console.print()
            yesno = rich_console.input("Would you like to try again? (Y/N): ")
            if yesno.lower() != "y":
                break
