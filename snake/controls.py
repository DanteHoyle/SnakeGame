import curses
# import logging
from snake.snake import HeadDirection, SnakeHead

class SnakeController:
    def __init__(self, window: curses.window, head_block: SnakeHead) -> None:
        self.window: curses.window = window
        self.head_block: SnakeHead = head_block

    def handle_input(self) -> None:
        ch = self.window.getch()

        # logging.debug(f'User Input: {ch}')

        match ch:
            case curses.KEY_UP:
                self.head_block.change_direction(HeadDirection.UP)
            case curses.KEY_DOWN:
                self.head_block.change_direction(HeadDirection.DOWN)
            case curses.KEY_LEFT:
                self.head_block.change_direction(HeadDirection.LEFT)
            case curses.KEY_RIGHT:
                self.head_block.change_direction(HeadDirection.RIGHT)
