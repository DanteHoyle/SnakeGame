#!/usr/bin/env python3
import logging

from snake.init import init_window, kill_window, parse_args
from snake.config import Config

if __name__ == "__main__":
    args = parse_args()

    config: Config = Config.from_config_file(args['config'])

    level = logging.INFO
    match args['verbosity']:
        case 'debug':
            level = logging.DEBUG
        case 'warn':
            level = logging.WARN
        case 'error':
            level = logging.ERROR

    logging.basicConfig(filename='log.txt',
                        level=level,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        filemode='w')

    window = init_window()


    from snake.engine import SnakeGame
    try:
        game = SnakeGame(window, config)
        game.run()
    except KeyboardInterrupt:
        logging.debug('Keyboard Interrupt Ignored')
    finally:
        kill_window(window)
