import logging
import curses

from snake.types import GameObject
from snake.config import Config
from snake.state import SharedGameState, Status
from snake.color import Color

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
