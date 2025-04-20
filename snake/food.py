import logging
import random
import curses

from snake.colors import Color
from snake.snake import SnakeHead
from snake.types import GameObject

class SnakeFood(GameObject):
    """Food object that when touched by SnakeHead, causes it to grow"""
    def __init__(self, head: SnakeHead, char: str) -> None:

        self.snake: SnakeHead = head

        self.boundary = head.boundary
        self.x: int = 0
        self.y: int = 0
        self.char: str = char

        self.color: Color = Color.SECONDARY

        self.pick_new_spot()

    def update(self) -> None:
        """Checks if snake overlaps the food object and grows the snake"""
        if self.collides_with_snake():
            self.snake.grow()
            self.pick_new_spot()

    def draw(self, window: curses.window) -> None:
        window.addch(self.y, self.x, self.char, self.color)

    def pick_new_spot(self) -> None:
        """Picks a new spot for the food item"""
        exclude = list(self.snake.body_positions())
        while True:
            bound_x, bound_y = self.boundary
            new_x = random.randint(1, bound_x - 1)
            new_y = random.randint(1, bound_y - 1)
            if (new_x, new_y) not in exclude:
                self.x = new_x
                self.y = new_y
                break
        logging.info(f'New Food at ({new_x}, {new_y})')

    def collides_with_snake(self) -> bool:
        """Returns true if the snake object and the food object share the same coordiantes"""
        return self.x == self.snake.x and self.y == self.snake.y
