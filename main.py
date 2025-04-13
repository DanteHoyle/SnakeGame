#!/usr/bin/env python3
import curses
import logging
from snake.snake import SnakeGame

def main(screen: curses.window):
    # hide the cursor during gameplay
    curses.curs_set(0)
    game = SnakeGame(screen)
    game.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename=f'log.txt',
                        format='%(asctime) %(name) %(levelname) %(message)',
                        datefmt='%H:%M:%S',
                        filemode='w')

    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        logging.debug('Keyboard Interrupt Ignored')
        pass
