import curses
# import logging
from snake.gameobjects import HeadDirection, SnakeHead
from snake.state import SharedGameState, Status

class SnakeController:
    def __init__(self, state: SharedGameState, head_block: SnakeHead) -> None:
        self.head_block: SnakeHead = head_block
        self.game_state: SharedGameState = state

    def handle_input(self, window: curses.window) -> None:
        ch: int = window.getch()

        self.handle_quit(ch)

        match self.game_state.state:
            case Status.GAMELOOP:
                self.handle_movement(ch)
            case _:
                pass

    def handle_movement(self, ch: int) -> None:
        if ch == curses.KEY_UP:
            self.head_block.change_direction(HeadDirection.UP)
        elif ch == curses.KEY_DOWN:
            self.head_block.change_direction(HeadDirection.DOWN)
        elif ch == curses.KEY_LEFT:
            self.head_block.change_direction(HeadDirection.LEFT)
        elif ch == curses.KEY_RIGHT:
            self.head_block.change_direction(HeadDirection.RIGHT)

    def handle_quit(self, ch: int) -> None:
        if ch in (ord('q'), ord('Q')):
            self.game_state.state = Status.EXIT
