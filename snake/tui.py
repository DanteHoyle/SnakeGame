import curses
import logging

from snake.state import GameState
from snake.types import GameObject
from snake.snake import SnakeHead

class UIOverlay(GameObject):
    def __init__(self, state: GameState, snake: SnakeHead, wall_char: str):
        self.game_state: GameState = state
        self.head_snake: SnakeHead = snake
        self.wall_char: str = wall_char

    def draw(self, window: curses.window):
        """Draws the score and the box around the playing field"""
        self.draw_score(window)
        self.draw_border(window)

    def draw_border(self, window: curses.window):
        """Draw edge of playable field border. Death logic is handled by the SnakeHead"""
        bound_x, bound_y = self.head_snake.bound_x, self.head_snake.bound_y
        for x in range(bound_x):
            window.addch(0, x, self.wall_char)
            window.addch(bound_y, x, self.wall_char)

        for y in range(1, bound_y):
            window.addch(y, 0, self.wall_char)
            window.addch(y, bound_x, self.wall_char)

    def draw_score(self, window: curses.window):
        """Calculates the score and draws it to the screen"""
        score_text = f'score: {self.head_snake.calculate_score()}'
        score_line = self.head_snake.bound_y + 1
        window.addstr(score_line, 0, score_text)

        logging.info(score_text)
