import curses
import logging

from snake.state import GameState
from snake.types import GameObject
from snake.snake import SnakeHead
from snake.colors import Color

class Boundary(GameObject):

    def __init__(self, snake: SnakeHead, v_char: str, h_char: str):
        self.head_snake: SnakeHead = snake
        self.vertical_char: str = v_char
        self.horizontal_char: str = h_char
        self.color = Color.BORDER

    def draw(self, window: curses.window):
        """Draw edge of playable field border. Death logic is handled by the SnakeHead"""
        bound_x, bound_y = self.head_snake.boundary
        for x in range(bound_x+1):
            window.addch(0, x, self.horizontal_char, self.color)
            window.addch(bound_y, x, self.horizontal_char, self.color)

        for y in range(1, bound_y):
            window.addch(y, 0, self.vertical_char, self.color)
            window.addch(y, bound_x, self.vertical_char, self.color)

class ScoreOverlay(GameObject):
    def __init__(self, state: GameState, snake: SnakeHead):
        self.game_state: GameState = state
        self.head_snake: SnakeHead = snake

        self.border_color: Color = Color.BORDER
        self.score_color: Color = Color.SECONDARY

    def draw(self, window: curses.window):
        """Draws the score and the box around the playing field"""
        self.draw_score(window)

    def draw_score(self, window: curses.window):
        """Calculates the score and draws it to the screen"""
        score_text = f'score: {self.head_snake.calculate_score()}'
        _, bound_y = self.head_snake.boundary
        score_line = bound_y + 1
        window.addstr(score_line, 0, score_text, self.score_color)

        logging.debug(score_text)
