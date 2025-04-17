import curses
import logging
from time import sleep

from snake.types import GameState, Config, Coordinate, BoundingArea
from snake.exceptions import InvalidGameStateError
from snake.controls import SnakeController
from snake.snake import SnakeHead
from snake.food import SnakeFood

class SnakeGame:
    """Main Game Class"""
    def __init__(self, window: curses.window, cfg: Config=Config()) -> None:
        """Initialize the main game objects."""
        self.window: curses.window = window
        self.window.nodelay(True)
        curses.curs_set(0)
        curses.noecho()

        self.screendelay: float = cfg.frame_delay 
        self.state: GameState = GameState.INIT
        self.cfg: Config = cfg
        logging.debug('SnakeGame initialized')

    def run(self) -> None:
        """Function which starts the game loop."""
        snake_start_pos: Coordinate = (self.cfg.start_x, self.cfg.start_y)
        food_start_pos: Coordinate = (self.cfg.food_start_x, self.cfg.food_start_y)
        playable_area: BoundingArea = (self.cfg.border_x, self.cfg.border_y)

        self.head_snake = SnakeHead(snake_start_pos,
                                    playable_area,
                                    self.cfg.snake_head_char,
                                    self.cfg.snake_body_char) 

        self.snake_food = SnakeFood(self.head_snake, food_start_pos, snake_start_pos, self.cfg.food_char)

        self.snake_controller: SnakeController = SnakeController(self.window, self.head_snake)
        self.state = GameState.GAMELOOP

        while self.state is not GameState.EXIT:
            self.main_loop()

    def main_loop(self) -> None:
        """Main Loop, this function gets called once per 'tick'."""
        match self.state:
            case GameState.GAMELOOP:
                self.snake_controller.handle_input()
                self.update()
                self.draw()
                sleep(self.screendelay)
            case _:
                raise InvalidGameStateError

    def update(self) -> None:
        """Updates all of the SnakeType objects held in self.game_objects."""
        self.head_snake.update()
        self.snake_food.update()

    def draw(self) -> None:
        self.window.clear()
        self.head_snake.draw(self.window)
        self.snake_food.draw(self.window)
        self.window.refresh()

