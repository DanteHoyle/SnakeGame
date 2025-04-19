#!/usr/bin/env python3
import curses
import logging
import argparse

from snake.init import init_window, kill_window, init_colors
from snake.exceptions import ImpossibleConfigError

if __name__ == "__main__":
    parser = argparse.ArgumentParser('BlockSnake')
    parser.add_argument('--verbosity', '-V', choices=('debug', 'info', 'warn', 'error'), default='info')
    args = parser.parse_args()
    match args.verbosity:
        case 'debug':
            level = logging.DEBUG
        case 'info':
            level = logging.INFO
        case 'warn':
            level = logging.WARN
        case 'error':
            level = logging.ERROR
        case _:
            raise ImpossibleConfigError('verbosity argument outside of possibilities')

    logging.basicConfig(filename='log.txt',
                        level=level,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        filemode='w')

    window = init_window()
    init_colors()

    from snake.engine import SnakeGame
    try:
        game = SnakeGame(window)
        game.run()
    except KeyboardInterrupt:
        logging.debug('Keyboard Interrupt Ignored')
    finally:
        kill_window(window)
