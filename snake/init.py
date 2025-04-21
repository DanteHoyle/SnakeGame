import argparse
import curses
import logging

def init_window() -> curses.window:
    """Handles creating the curses window."""
    window = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    window.keypad(True)
    window.nodelay(True)
    curses.start_color()
    curses.use_default_colors()

    logging.debug('Finished initializing window')
    return window

def kill_window(window: curses.window) -> None:
    """Handles closing the curses window."""
    curses.nocbreak()
    window.keypad(False)
    curses.echo()
    curses.endwin()
    logging.debug('Finished killing window')

def parse_args() -> dict[str, str]:
    """Parses any arguments passed as CLI and returns a dictionary of config values."""
    parser = argparse.ArgumentParser('BlockSnake')
    parser.add_argument('--verbosity', '-V', choices=('debug', 'info', 'warn', 'error'), default='info')
    parser.add_argument('--config', '-C', default='data/config.json', type=str, help = 'Path of the config file to use')
    args = parser.parse_args()

    args_as_dict = vars(args)
    return args_as_dict
