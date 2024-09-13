from rich.text import Text
from rich.table import Table
from ttg.core.evaluator import TruthTable


def format_bool(value: bool) -> Text:
    "Formats boolean value for console display"

    text = Text(str(value))
    text.stylize("italic")

    if value:
        text.stylize("green")
    else:
        text.stylize("red")

    return text


def format(values: TruthTable, title="Truth Table") -> Table:
    "Formats the truth-table for console display"

    table = Table(title=title)

    # Add formulas of the truth table as columns
    columns = list(values.keys())
    for column in columns:
        table.add_column(column, justify="center")

    # Gather the values of the formulas for each row/index
    row_count = len(values[columns[0]])
    for i in range(row_count):
        row = map(lambda column: values[column][i], columns)
        row_str = map(lambda value: format_bool(value), row)
        table.add_row(*row_str)

    return table
