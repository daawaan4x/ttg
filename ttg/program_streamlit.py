from __future__ import annotations

import re

import pandas as pd
import streamlit as st

from ttg.core.evaluator import evaluate
from ttg.core.lexer import Token, tokenize
from ttg.core.parser import ParserError, parse


def page() -> None:
    st.markdown("""
# 🟰 TTG
> by *Theone Genesis Eclarin* (Github @ [daawaan4x](https://github.com/daawaan4x))

A Truth Table Generator for Propositional Logic Formulas made with Python.
    """)

    try:
        program()
    except Exception as exc:
        st.exception(exc)

    st.divider()
    st.markdown("""
## Features

- **Supported Logical Operators**: In order of precedence
    - `NOT`, `not`, `!`, `~`, `¬`
    - `AND`, `and`, `&`, `&&`, `^`, `∧`
    - `OR`, `or`, `|`, `||`, `v`, `∨`
    - `THEN`, `then`, `IF`, `if`, `>`, `->`, `→`
    - `ONLY IF`, `only if`, `IFF`, `iff`, `==`, `<>`, `<->`, `↔`
- **Complex Formulas**: Input nested formulas using parenthesis `(...)`
    - **Unlimited Variables**: Add any amount of variables using any combination of alphabet `a-z,A-Z` letters.
    """)  # noqa: E501, RUF001


def program() -> None:
    inspect = st.toggle(label="Inspect Mode")

    formula = st.text_input(label="Formula")
    formula.strip()

    if not formula:
        return

    tokens = tokenize(formula)
    if inspect:
        st.json({"formula": formula})
        st.json(tokens)
    validate_tokens(formula, tokens)

    try:
        tree = parse(tokens)
    except ParserError as exc:
        st.error(highlight_tokens(formula, [exc.token]))
        raise
    if inspect:
        st.json(tree.json())

    truth_table = evaluate(tokens, tree)
    dataframe = pd.DataFrame(truth_table)
    dataframe.index += 1  # type: ignore  # noqa: PGH003
    st.dataframe(dataframe)  # type: ignore  # noqa: PGH003


def validate_tokens(formula: str, tokens: list[Token]) -> None:
    """Check invalid tokens and print the error."""
    invalid_tokens = list(filter(lambda x: x.type == "invalid", tokens))

    # skip funciton if no invalid tokens
    if len(invalid_tokens) == 0:
        return

    st.error(highlight_tokens(formula, invalid_tokens))
    raise Exception("Invalid Token(s) Found", formula)


def highlight_tokens(formula: str, tokens: list[Token]) -> str:
    pattern = r"(" + "|".join(re.escape(tok.value) for tok in tokens) + r")"
    return re.sub(pattern, r":red-background[\1]", formula)


page()
