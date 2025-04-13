import curses
from datetime import datetime, timedelta
from snake.block import Direction, SnakeHead

class SnakeController:
    def __init__(self, window: curses.window, head_block: SnakeHead) -> None:
        self.window: curses.window = window
        self.head_block: SnakeHead = head_block

    def handle_input(self) -> None:
        ch = self.window.getch()

        match ch:
            case curses.KEY_UP:
                self.head_block.change_direction(Direction.UP)
            case curses.KEY_DOWN:
                self.head_block.change_direction(Direction.DOWN)
            case curses.KEY_LEFT:
                self.head_block.change_direction(Direction.LEFT)
            case curses.KEY_RIGHT:
                self.head_block.change_direction(Direction.RIGHT)

    def input_poller(self, delay: float) -> None:
        start_time: datetime = datetime.now()
        time_since_start: float = 0.0

        while time_since_start < delay:
            self.handle_input()
            current_time: datetime = datetime.now()
            delta: timedelta = current_time - start_time
            time_since_start = delta.total_seconds()
