import curses
import logging
from time import sleep
from enum import Enum, auto

from snake.exceptions import InvalidGameState
from snake.controls import SnakeController
from snake.block import SnakeBlock, SnakeHead

type SnakeBody = SnakeBlock | SnakeHead

class GameState(Enum):
    INIT = auto()
    GAMELOOP = auto()
    EXIT = auto()

class SnakeGame:
    """Main Game Class"""
    def __init__(self, window: curses.window) -> None:
        """
        Initialize the main game objects
        Arguments:
        screen - a curses window object
        """
        self.window: curses.window = window
        self.window.nodelay(True)

        self.screendelay: float = 0.1
        self.state: GameState = GameState.INIT
        self.blocks: list[SnakeBody] = []

        head_snake = SnakeHead(10, 10)

        self.blocks.append(head_snake)
        self.snake_controller: SnakeController = SnakeController(self.window, head_snake)
        logging.debug('SnakeGame initialized')

    def run(self) -> None:
        self.state = GameState.GAMELOOP
        while self.state is not GameState.EXIT:
            self.main_loop()
            sleep(self.screendelay) # TEMPORARY

    def main_loop(self) -> None:
        match self.state:
            case GameState.GAMELOOP:
                self.snake_controller.input_poller(self.screendelay)
                self.update()
                self.draw()
            case _:
                raise InvalidGameState

    def draw(self) -> None:
        self.window.clear()

        for block in self.blocks:
            block.draw(self.window)

        self.window.refresh()

    def update(self) -> None:
        for block in self.blocks:
            block.update()
