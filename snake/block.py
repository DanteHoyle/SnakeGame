from enum import Enum, auto
import logging
import curses

class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()

class SnakeObj:
    id_counter: int = 0
    def __init__(self, spawn_x: int, spawn_y: int, char: str):
        SnakeObj.id_counter += 1
        self.id = SnakeObj.id_counter

        self.x = spawn_x
        self.y = spawn_y
        self.char = char
        logging.info(f'New SnakeObj {type(self)} ({spawn_x}, {spawn_y}) char={self.char}')

    def draw(self, screen: curses.window) -> None:
        screen.addch(self.y, self.x, self.char)

    def update(self) -> None:
        return

    def set_position(self, new_x: int, new_y: int) -> None:
        self.x = new_x
        self.y = new_y

class SnakeFood(SnakeObj):
    def __init__(self, spawn_x: int, spawn_y: int):
        super().__init__(spawn_x, spawn_y, '@')


class SnakeHead(SnakeObj):
    def __init__(self, spawn_x: int, spawn_y: int, direction: Direction=Direction.RIGHT) -> None:
        super().__init__(spawn_x, spawn_y, '#')
        # Only the head block has a direction. Child blocks have direction set to None
        self.direction: Direction = direction

    def update(self) -> None:
        match self.direction:
            case Direction.UP:
                self.y -= 1
            case Direction.DOWN:
                self.y += 1
            case Direction.RIGHT:
                self.x += 1
            case Direction.LEFT:
                self.x -= 1

    def change_direction(self, new_direction: Direction) -> bool:
        """
        Attempst to change the direction of the lead block
        """
        veritcal_axis = (Direction.UP, Direction.DOWN)
        horizontal_axis = (Direction.LEFT, Direction.RIGHT)

        if self.direction in veritcal_axis and new_direction in veritcal_axis:
            return False

        if self.direction in horizontal_axis and new_direction in horizontal_axis:
            return False

        self.direction = new_direction
        logging.debug(f'SnakeBlock({self.id=}) changed direction to {new_direction}')
        return True

class SnakeBlock(SnakeObj):
    """
    This represents a piece of the snake which the player controls
    """
    def __init__(self, spawn_x: int, spawn_y: int):
        super().__init__(spawn_x, spawn_y, '#')
        # The last block will have next_block be None
        self.next_block: SnakeBlock|None = None
        self.last_x: int = spawn_x
        self.last_y: int = spawn_y

    def set_position(self, new_x: int, new_y: int) -> None:
        self.last_x = self.x
        self.last_y = self.y
        self.x = new_x
        self.y = new_y

    def grow(self) -> None:
        if not self.next_block:
            self.next_block = SnakeBlock(self.last_x, self.last_y)
        else:
            self.next_block.grow()

