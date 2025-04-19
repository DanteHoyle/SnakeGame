import curses
import logging

def init_window() -> curses.window:
    window = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    window.keypad(True)
    window.nodelay(True)

    logging.debug('Window Initialized!')
    return window

def init_colors():
    logging.debug('Colors Initialized!')
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)

def kill_window(window: curses.window) -> None:
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()
