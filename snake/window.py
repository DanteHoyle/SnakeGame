import curses

from snake.colors import init_colors

def init_window() -> curses.window:
    window = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    window.keypad(True)
    window.nodelay(True)
    init_colors()
    return window

def kill_window(window: curses.window) -> None:
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()

