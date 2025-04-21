import curses
import logging
import time

from snake.config import Config
from snake.colors import Color, ColorManager
from snake.types import GameObject
from snake.controls import SnakeController
from snake.snake import SnakeHead
from snake.food import SnakeFood
from snake.tui import Boundary, ScoreOverlay
from snake.state import GameState, States

class SnakeGame:
    """Main Game Class"""
    def __init__(self, window: curses.window, cfg: Config) -> None:
        """Initialize the main game objects."""
        self.window: curses.window = window

        self.screendelay: float = cfg.frame_delay 
        self.state: GameState = GameState()
        self.cfg: Config = cfg
        self.game_objects: list["GameObject"] = []
        self.color_manager: ColorManager = ColorManager()
        logging.debug('SnakeGame initialized')

    def run(self) -> None:
        """Function which starts the game loop."""
        head_snake = SnakeHead(self.cfg) 
        snake_food = SnakeFood(head_snake, self.cfg.food_char)
        score = ScoreOverlay(self.state, head_snake)
        boundary = Boundary(head_snake, self.cfg.vertical_wall_char, self.cfg.horizontal_wall_char)

        self.game_objects = [head_snake,
                             snake_food,
                             score,
                             boundary]

        self.snake_controller: SnakeController = SnakeController(self.window, head_snake)

        self.state.enter_gameloop()

        while self.state != States.EXIT:
            match self.state:
                case States.GAMELOOP:
                    self.gameloop()

    def gameloop(self) -> None:
        """Main Loop, this function gets called once per 'tick'."""
        self.update()
        self.draw()

    def update(self) -> None:
        """Updates all of the SnakeType objects held in self.game_objects."""
        self.snake_controller.handle_input()
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

