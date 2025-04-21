import logging
import curses
from typing import Generator

from snake.state import SharedGameState, Status
from snake.types import BoundingArea, Coordinate, GameObject, HeadDirection
from snake.colors import Color, ColorIfColorsEnabled
from snake.config import Config

class SnakeBody(GameObject):
    """This represents a piece of the snake which the player controls."""
    def __init__(self, spawn_x: int, spawn_y: int, char: str, color: ColorIfColorsEnabled=None):
        self.x: int = spawn_x
        self.last_x: int = spawn_x
        self.y = spawn_y
        self.last_y = spawn_y
        # The last block will have next_block be None
        self.next: SnakeBody|None = None

        # Graphical Elements
        self.char: str = char
        self.body_char: str = self.char
        self.color: ColorIfColorsEnabled = color

    def __iter__(self) -> Generator["SnakeBody", None, None]:
        s = self
        while s:
            yield s
            s = s.next

    def draw(self, window: curses.window) -> None:
        if self.color:
            window.addch(self.y, self.x, self.char, self.color)
        else:
            window.addch(self.y, self.x, self.char)

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
        if next := self.next:
            next.grow()
        else:
            self.next = SnakeBody(self.last_x, self.last_y, self.body_char, self.color)

    def collides_with(self, other: "SnakeBody") -> bool:
        return self.x == other.x and self.y == other.y

    def calculate_score(self) -> int:
        """score = number of fruit eaten"""
        if self.next:
            return sum(1 for _ in self.next)
        return 0

class SnakeHead(SnakeBody):
    """The main Game Object that the player controls."""
    def __init__(self, config: Config, state: SharedGameState) -> None:
        super().__init__(config.start_x, config.start_y, config.snake_head_char, Color.PRIMARY)
        # Overwrite headchar set by constructor.
        self.body_char: str = config.snake_body_char
        self.direction: HeadDirection = HeadDirection.RIGHT
        self.boundary: BoundingArea = BoundingArea((config.border_x, config.border_y))
        self.game_state: SharedGameState = state

    def update(self) -> None:
        def gameloop() -> None:
            self.move_one_space()
            if self.collides_with_body():
                self.die()

        match self.game_state.state:
            case Status.GAMELOOP:
                gameloop()

    def grow(self) -> None:
        self.game_state.score += 1
        return super().grow()
        # if next := self.next:
        #     next.grow()
        # else:
        #     self.next = SnakeBody(self.last_x, self.last_y, self.body_char, self.color)

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
        """Creates a list of Coordinates recording all x,y positions of the snakes body."""
        positions: list[Coordinate] = []
        for s in self:
            positions.append((s.x, s.y))

        return positions

    def die(self) -> None:
        raise RuntimeError("DEAD")

    def next_position(self) -> Coordinate:
        next_x = self.x
        next_y = self.y
        match self.direction:
            case HeadDirection.UP:
                next_y -= 1
            case HeadDirection.DOWN:
                next_y += 1
            case HeadDirection.RIGHT:
                next_x += 1
            case HeadDirection.LEFT:
                next_x -= 1

        return (next_x, next_y)

    def move_one_space(self) -> None:
        """
        Checks if it's safe to move another space before hitting a boundary
        Then checks
        """
        next_x, next_y = self.next_position()

        if not self.boundary.contains_coordinate((next_x, next_y)):
            self.die()

        self.set_position(next_x, next_y)

    def collides_with_body(self) -> SnakeBody|None:
        """
        Returns a SnakeBody object if the SnakeHead is intersecting any SnakeBody pieces,
        otherwise, it reurns None.
        """
        for body in self:
            if body is self:
                continue
            if self.collides_with(body):
                return body
        return None
