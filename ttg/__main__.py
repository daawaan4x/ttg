import sys
import os
import pathlib

sys.path.append(os.getcwd())
sys.path.append(
    pathlib.Path(
        os.path.dirname(os.path.realpath(__file__))
    ).parent.absolute()
)

from ttg.command import command

if __name__ == '__main__':
    command()
