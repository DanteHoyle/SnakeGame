import logging
import curses
from typing import Generator

from snake.types import BoundingArea, Coordinate, HeadDirection 

class SnakeBody:
    """This represents a piece of the snake which the player controls."""
    def __init__(self, spawn_x: int, spawn_y: int, char: str):
        self.x = spawn_x
        self.last_x = spawn_x
        self.y = spawn_y
        self.last_y = spawn_y
        # The last block will have next_block be None
        self.next: SnakeBody|None = None
        self.last_x: int = spawn_x
        self.last_y: int = spawn_y
        self.char = char
        self.body_char = self.char

    def __iter__(self) -> Generator["SnakeBody", None, None]:
        s = self
        while s:
            yield s
            s = s.next

    def draw(self, screen: curses.window) -> None:
        for s in self:
            screen.addch(s.y, s.x, s.char)

    def set_position(self, new_x: int, new_y: int) -> None:
        self.last_x = self.x
        self.last_y = self.y
        self.x = new_x
        self.y = new_y

        if next := self.next:
            next.set_position(self.last_x, self.last_y)

    def grow(self) -> None:
        if next := self.next:
            next.grow()
        else:
            self.next = SnakeBody(self.last_x, self.last_y, self.body_char)

    def collides_with(self, other: "SnakeBody") -> bool:
        return self.x == other.x and self.y == other.y

class SnakeHead(SnakeBody):
    def __init__(self,
                 spawn: Coordinate,
                 bounding: BoundingArea,
                 head_char: str,
                 body_char: str) -> None:
        spawn_x, spawn_y = spawn
        super().__init__(spawn_x, spawn_y, head_char)
        # Overwrite headchar set by constructor.
        self.body_char: str = body_char
        self.direction: HeadDirection = HeadDirection.RIGHT

        bound_x, bound_y = bounding
        self.bound_x: int = bound_x
        self.bound_y: int = bound_y

    def update(self) -> None:
        logging.debug(f'x={self.x}, y={self.y} | {self.last_x=}, {self.last_y=}')
        self.move_one_space()

    def change_direction(self, new_direction: HeadDirection) -> bool:
        """Attempst to change the direction of the lead block."""
        vertical_axis = (HeadDirection.UP, HeadDirection.DOWN)
        horizontal_axis = (HeadDirection.LEFT, HeadDirection.RIGHT)

        if self.direction in vertical_axis and new_direction in vertical_axis:
            return False

        if self.direction in horizontal_axis and new_direction in horizontal_axis:
            return False

        self.direction = new_direction
        self.char = self.direction.value
        logging.debug(f'Snake Head changed direction to {new_direction}')
        return True

    def body_positions(self) -> list[Coordinate]:
        """Generator function yields the coordinate of every snake body part"""
        positions: list[Coordinate] = []
        for s in self:
            positions.append((s.x, s.y))

        return positions

    def move_one_space(self):
        match self.direction:
            case HeadDirection.UP:
                self.set_position(self.x, self.y - 1)
            case HeadDirection.DOWN:
                self.set_position(self.x, self.y + 1)
            case HeadDirection.RIGHT:
                self.set_position(self.x + 1, self.y)
            case HeadDirection.LEFT:
                self.set_position(self.x - 1, self.y)
