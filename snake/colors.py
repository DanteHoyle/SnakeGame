import curses
import logging
from enum import IntEnum

class Color(IntEnum):
    PRIMARY = curses.color_pair(1)
    SECONDARY = curses.color_pair(2)

type ColorIfColorsEnabled = Color|None
