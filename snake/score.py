import logging
import curses

from snake.types import GameObject
from snake.config import Config
from snake.state import SharedGameState
from snake.color import Color

class Score(GameObject):
    def __init__(self, config: Config, state: SharedGameState):
        self.game_state: SharedGameState = state
        self.score_color: Color = Color.SECONDARY
        self.score_text_y_pos = config.border_y + 1

        logging.info('Score Overlay Created')

    def draw(self, window: curses.window):
        """Draws the score and the box around the playing field."""
        self.draw_score(window)

    def draw_score(self, window: curses.window):
        """Calculates the score and draws it to the screen."""
        score_text = f'score: {self.game_state.score}'
        window.addstr(self.score_text_y_pos, 0, score_text, self.score_color)
