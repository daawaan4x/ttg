import os
import sys
from pathlib import Path

sys.path.append(os.getcwd())  # noqa: PTH109
sys.path.append(
    Path(os.path.dirname(os.path.realpath(__file__))).parent.absolute().__str__(),  # noqa: PTH120
)

from ttg.command import command

if __name__ == "__main__":
    command()
