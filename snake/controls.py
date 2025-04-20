import curses
# import logging
from snake.snake import HeadDirection, SnakeHead

class SnakeController:
    def __init__(self, window: curses.window, head_block: SnakeHead) -> None:
        self.window: curses.window = window
        self.head_block: SnakeHead = head_block

    def handle_input(self) -> None:
        ch: int = self.window.getch()

        if ch == curses.KEY_UP:
            self.head_block.change_direction(HeadDirection.UP)
        elif ch == curses.KEY_DOWN:
            self.head_block.change_direction(HeadDirection.DOWN)
        elif ch == curses.KEY_LEFT:
            self.head_block.change_direction(HeadDirection.LEFT)
        elif ch == curses.KEY_RIGHT:
            self.head_block.change_direction(HeadDirection.RIGHT)
        elif ch in (ord('q'), ord('Q')):
            self.head_block.die()

