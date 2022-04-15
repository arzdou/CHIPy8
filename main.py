import os
import sys

from chipy8.run import run

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

if __name__ == "__main__":
    sys.exit(run("roms/test_opcode.ch8"))