#!/usr/bin/env python3
import curses
import logging
import argparse

from snake.engine import SnakeGame
from snake.exceptions import ImpossibleConfigError
from snake.window import init_window, kill_window

def main(screen: curses.window):
    # hide the cursor during gameplay
    game = SnakeGame(screen)
    game.run()

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

    try:
        main(window)
    except KeyboardInterrupt:
        logging.debug('Keyboard Interrupt Ignored')
    finally:
        kill_window(window)

