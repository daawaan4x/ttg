from rich.table import Table
from rich.text import Text

from ttg.core.evaluator import TruthTable


def format_bool(value: bool) -> Text:
    """Format boolean value for console display."""
    text = Text(str(value))
    text.stylize("italic")

    if value:
        text.stylize("green")
    else:
        text.stylize("red")

    return text


def format_truth_table(values: TruthTable, title: str = "Truth Table") -> Table:
    """Format the truth-table for console display."""
    table = Table(title=title)

    # Add formulas of the truth table as columns
    columns = list(values.keys())
    for column in columns:
        table.add_column(column, justify="center")

    # Gather the values of the formulas for each row/index
    row_count = len(values[columns[0]])
    for i in range(row_count):
        row = (values[column][i] for column in columns)
        row_str = (format_bool(value) for value in row)
        table.add_row(*row_str)

    return table
