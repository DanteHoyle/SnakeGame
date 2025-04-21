import curses
import logging
import time

from snake.config import Config
from snake.color import Color, ColorManager
from snake.types import GameObject
from snake.controls import SnakeController
from snake.snake import SnakeHead
from snake.food import SnakeFood
from snake.boundary import Boundary
from snake.text import TextManager
from snake.state import SharedGameState, Status

class SnakeGame:
    """Main Game Class"""
    def __init__(self, window: curses.window, cfg: Config) -> None:
        """Initialize the main game objects."""
        self.window: curses.window = window

        self.screendelay: float = cfg.frame_delay 
        self.game_state: SharedGameState = SharedGameState()
        self.cfg: Config = cfg
        self.game_objects: list["GameObject"] = []
        self.color_manager: ColorManager = ColorManager(cfg.color_palette)
        logging.debug('SnakeGame initialized')

    def run(self) -> None:
        """Function which starts the game loop."""
        head_snake = SnakeHead(self.cfg, self.game_state) 

        self.game_objects = [
            head_snake,
            SnakeFood(self.cfg, head_snake),
            TextManager(self.cfg, self.game_state),
            Boundary(self.cfg)
        ]

        self.snake_controller: SnakeController = SnakeController(self.game_state, head_snake)

        self.game_state.state = Status.GAMELOOP

        while self.game_state.state != Status.EXIT:
            self.update()
            self.draw()

    def update(self) -> None:
        """Updates all of the SnakeType objects held in self.game_objects."""
        self.snake_controller.handle_input(self.window)
        for obj in self.game_objects:
            obj.update()

    def draw(self) -> None:
        """Draw all game objects to the screen and sleep for a fraction of a second."""
        self.window.erase()

        for obj in self.game_objects:
            obj.draw(self.window)
        self.window.bkgd(' ', Color.EMPTY)
        self.window.refresh()
        time.sleep(self.screendelay)

