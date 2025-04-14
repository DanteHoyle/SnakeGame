import curses
import logging
from time import sleep
from enum import Enum, auto

from snake.exceptions import InvalidGameStateError
from snake.controls import SnakeController
from snake.snake import SnakeHead, SnakeType, SnakeObject

class GameState(Enum):
    INIT = auto()
    GAMELOOP = auto()
    EXIT = auto()

class SnakeGame:
    """Main Game Class"""
    def __init__(self, window: curses.window) -> None:
        """Initialize the main game objects."""
        self.window: curses.window = window
        self.window.nodelay(True)
        curses.curs_set(0)
        curses.noecho()

        self.screendelay: float = 0.1
        self.game_objects: list[SnakeType] = []
        self.state: GameState = GameState.INIT
        logging.debug('SnakeGame initialized')

    def run(self) -> None:
        """Function which starts the game loop."""
        self.game_objects = SnakeObject.all
        head_snake = SnakeHead(10, 10, 40, 40, '#')
        self.snake_controller: SnakeController = SnakeController(self.window, head_snake)
        self.state = GameState.GAMELOOP

        while self.state is not GameState.EXIT:
            self.main_loop()

    def main_loop(self) -> None:
        match self.state:
            case GameState.GAMELOOP:
                self.snake_controller.handle_input()
                self.update()
                self.draw()
                sleep(self.screendelay)
            case _:
                raise InvalidGameStateError

    def update(self) -> None:
        for block in self.game_objects:
            block.update()

    def draw(self) -> None:
        self.window.clear()

        for block in self.game_objects:
            block.draw(self.window)

        self.window.refresh()

