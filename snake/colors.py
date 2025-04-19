import curses
from enum import IntEnum

def init_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)

class Colors(IntEnum):
    PRIMARY = 1
    SECONDARY = 2
