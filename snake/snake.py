import logging
import curses
from typing import Generator
from enum import StrEnum

from snake.state import SharedGameState, Status
from snake.types import BoundingArea, Coordinate, GameObject
from snake.color import Color
from snake.config import Config

class SnakeBody(GameObject):
    """This represents a piece of the snake which the player controls."""
    def __init__(self, spawn_x: int, spawn_y: int, char: str):
        self.x: int = spawn_x
        self.last_x: int = spawn_x
        self.y = spawn_y
        self.last_y = spawn_y
        # The last block will have next_block be None
        self.next: SnakeBody|None = None
        # Graphical Elements
        self.char: str = char
        self.body_char: str = self.char
        self.color = Color.PRIMARY

        logging.info(f'New SnakeBody created at ({self.x}, {self.y})')

    def __iter__(self) -> Generator["SnakeBody", None, None]:
        s = self
        while s:
            yield s
            s = s.next

    def draw(self, window: curses.window) -> None:
        window.addch(self.y, self.x, self.char, self.color)

        if self.next:
            self.next.draw(window)

    def set_position(self, new_x: int, new_y: int) -> None:
        self.last_x = self.x
        self.last_y = self.y
        self.x = new_x
        self.y = new_y

        if next := self.next:
            next.set_position(self.last_x, self.last_y)

    def grow(self) -> None:
        """This method causes the snake to grow by one SnakeBody"""
        if next := self.next:
            next.grow()
        else:
            self.next = SnakeBody(self.last_x, self.last_y, self.body_char)

class HeadDirection(StrEnum):
    """The mouth faces the direciton the snake is going."""
    UP = 'V'
    DOWN = 'Λ'
    LEFT = '>'
    RIGHT = '<'

class SnakeHead(SnakeBody):
    """The main Game Object that the player controls."""
    def __init__(self, config: Config, state: SharedGameState) -> None:
        super().__init__(config.start_x, config.start_y, config.snake_head_char)
        # Overwrite headchar set by constructor.
        self.body_char: str = config.snake_body_char
        self.direction: HeadDirection = HeadDirection.RIGHT
        self.boundary: BoundingArea = BoundingArea((config.border_x, config.border_y))
        self.game_state: SharedGameState = state

        logging.info(f'New SnakeHead created at ({self.x}, {self.y})')

    def update(self) -> None:
        if self.game_state.state is Status.GAMELOOP:
            next_coordinate = self.next_position()
            x, y = next_coordinate

            if next_coordinate in self.snake_body_coordinates():
                logging.info(f'The snake collided with itself at ({x=}, {y=}) and died')
                self.die()
            elif not self.boundary.contains_coordinate(next_coordinate):
                logging.info(f'The snake collided with the barrier at ({x=}, {y=}) and died')
                self.die()
            else:
                self.set_position(x, y)

    def grow(self) -> None:
        """Increases the score by one when the head snake grows."""
        self.game_state.score += 1
        logging.info(f'The Snake Head has grown and the score has increased to {self.game_state.score}')
        return super().grow()

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

    def die(self) -> None:
        self.game_state.state = Status.DEADSNAKE
        logging.info('The snake has died')
        for body in self:
            body.color = Color.SECONDARY
            body.char = 'X'

    def next_position(self) -> Coordinate:
        match self.direction:
            case HeadDirection.UP:
                return (self.x, self.y-1)
            case HeadDirection.DOWN:
                return (self.x, self.y+1)
            case HeadDirection.RIGHT:
                return (self.x+1, self.y)
            case HeadDirection.LEFT:
                return (self.x-1, self.y)

    def snake_body_coordinates(self) -> list[Coordinate]:
        return list([(snake.x, snake.y) for snake in self])
