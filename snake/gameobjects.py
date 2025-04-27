import logging
import curses
from typing import Generator
from enum import StrEnum
import random

from snake.state import SharedGameState, Status
from snake.color import Color
from snake.config import Config

type Coordinate = tuple[int, int]

class BoundingArea(tuple[int, int]):
    """Used by objects to track the playable area"""
    def contains_coordinate(self, coord: Coordinate) -> bool:
        bx, by = self
        cx, cy = coord

        return (cx >= 1 and cx <= bx-1 and cy >= 1 and cy <= by-1)

class GameObject:
    """Base Class Used Objects that are drawn to the screen"""
    def update(self):
        return
    def draw(self, window: curses.window):
        raise NotImplementedError(window)

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

class SnakeFood(GameObject):
    """Food object that when touched by SnakeHead, causes it to grow."""
    def __init__(self, config: Config, head: SnakeHead) -> None:

        self.snake: SnakeHead = head

        self.boundary = head.boundary
        self.x: int = config.food_start_x
        self.y: int = config.food_start_y
        self.char: str = config.food_char

        self.color: Color = Color.SECONDARY

        self.pick_new_spot()

    def update(self) -> None:
        """Checks if snake overlaps the food object and grows the snake."""
        if self.collides_with_snake():
            self.snake.grow()
            self.pick_new_spot()

    def draw(self, window: curses.window) -> None:
        window.addch(self.y, self.x, self.char, self.color)

    def pick_new_spot(self) -> None:
        """Picks a new spot for the food item."""
        exclude: list[Coordinate] = []
        for s in self.snake:
            exclude.append((s.x, s.y))

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
        """Returns true if the snake object and the food object share the same coordiantes."""
        return self.x == self.snake.x and self.y == self.snake.y

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

class TextManager(GameObject):
    def __init__(self, config: Config, state: SharedGameState):
        self.game_state = state
        self.text_objects: list['GameObject'] = [
            Score(config, state)
        ]

    def update(self) -> None:
        if self.game_state.state is Status.DEADSNAKE:
            self.create_lose_screen()
            self.game_state.state = Status.SHOWSCORE

        for obj in self.text_objects:
            obj.update()

    def draw(self, window: curses.window) -> None:
        for obj in self.text_objects:
            obj.draw(window)

    def create_lose_screen(self):
        self.text_objects.append(Text('You lose!', 4, 4, Color.TERTIARY))

class Score(GameObject):
    def __init__(self, config: Config, state: SharedGameState):
        self.game_state: SharedGameState = state
        self.highlight_color: Color = Color.SECONDARY
        self.text_color: Color = Color.TERTIARY
        self.score_text_y_pos = config.border_y + 1

        logging.info('Score Overlay Created')

    def draw(self, window: curses.window):
        """Draws the score and the box around the playing field."""
        score_text = 'score: '
        score = str(self.game_state.score)
        window.addstr(self.score_text_y_pos, 0, score_text, self.text_color)
        window.addstr(self.score_text_y_pos, len(score_text), score, self.highlight_color)

class Text(GameObject):
    def __init__(self, text: str, x: int, y: int, color: Color, visible: bool=True):
        self.text: str = text
        self.x: int = x
        self.y: int = y
        self.color: Color = color
        self.visible = visible

    def draw(self, window: curses.window):
        if self.visible:
            window.addstr(self.y, self.x, self.text, self.color)
