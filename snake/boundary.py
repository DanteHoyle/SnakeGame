import curses
import logging

from snake.config import Config
from snake.types import GameObject
from snake.color import Color

class Boundary(GameObject):
    def __init__(self, config: Config):
        self.vertical_char: str = config.vertical_wall_char
        self.horizontal_char: str = config.horizontal_wall_char
        self.color = Color.BORDER
        self.boundary = (config.border_x, config.border_y)

        logging.info('Boundary Object Created')

    def draw(self, window: curses.window):
        """Draw edge of playable field border. Death logic is handled by the SnakeHead."""
        bound_x, bound_y = self.boundary
        for x in range(bound_x+1):
            window.addch(0, x, self.horizontal_char, self.color)
            window.addch(bound_y, x, self.horizontal_char, self.color)

        for y in range(1, bound_y):
            window.addch(y, 0, self.vertical_char, self.color)
            window.addch(y, bound_x, self.vertical_char, self.color)
