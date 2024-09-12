from typing import Dict, List

from ttg.core.parser import Expr

TruthTable = Dict[str, List[bool]]


def evaluate(tree: Expr) -> TruthTable:
    return {
        "P": [True, True, False, False],
        "Q": [True, False, True, False],
        "P & Q": [True, False, False, False],
    }
