import logging
import random
import curses

from snake.snake import SnakeHead
from snake.types import Coordinate, BoundingArea

class SnakeFood:
    """Food object that when touched by SnakeHead, causes it to grow"""
    def __init__(self, head: SnakeHead, bounding: BoundingArea, excluded: Coordinate, char: str) -> None:

        self.snake: SnakeHead = head

        bound_x, bound_y = bounding
        self.bound_x: int = bound_x
        self.bound_y: int = bound_y
        self.x: int = 0
        self.y: int = 0
        self.char: str = char
        self.pick_new_spot([excluded])

    def update(self) -> None:
        if self.collides_with_snake():
            self.snake.grow()
            exclude = list(self.snake.body_positions())
            self.pick_new_spot(exclude)

    def draw(self, screen: curses.window) -> None:
        screen.addch(self.y, self.x, self.char)

    def pick_new_spot(self, excluded: list[Coordinate]=[]) -> None:
        """Picks a new spot for the food item"""
        logging.debug(f'New Spot Exclude List:\n{excluded=}')
        while True:
            new_x = random.randint(0, self.bound_x)
            new_y = random.randint(0, self.bound_y)
            if (new_x, new_y) not in excluded:
                self.x = new_x
                self.y = new_y
                break
        logging.info(f'New Food at ({new_x}, {new_y})')

    def collides_with_snake(self) -> bool:
        return self.x == self.snake.x and self.y == self.snake.y
