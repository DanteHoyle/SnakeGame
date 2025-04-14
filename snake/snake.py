from enum import Enum, auto
import logging
import curses
import random

class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()

type SnakeType = SnakeObject | SnakeFood | SnakeHead | SnakeBody

class SnakeObject:
    all: list[SnakeType] = []
    def __init__(self, spawn_x: int, spawn_y: int, char: str) -> None:
        self.x = spawn_x
        self.last_x = spawn_x
        self.y = spawn_y
        self.last_y = spawn_y

        self.char = char
        logging.info(f'New SnakeObj {type(self)} ({spawn_x}, {spawn_y}) char={self.char}')
        SnakeObject.all.append(self)

    def draw(self, screen: curses.window) -> None:
        screen.addch(self.y, self.x, self.char)

    def update(self) -> None:
        return

    def set_position(self, new_x: int, new_y: int) -> None:
        self.last_x = self.x
        self.last_y = self.y
        self.x = new_x
        self.y = new_y

    def collides_with(self, other: SnakeType) -> bool:
        return self.x == other.x and self.y == other.y

type Coordinate = tuple[int, int]

class SnakeFood(SnakeObject):
    def __init__(self, bound_x: int, bound_y: int, exclude_x: int, exclude_y: int):
        self.bound_x = bound_x
        self.bound_y = bound_y
        exclude_coord = (exclude_x, exclude_y)

        self.pick_new_spot([exclude_coord])
        super().__init__(self.x, self.y, '@')

    def pick_new_spot(self, excluded: list[Coordinate]=[]) -> None:
        logging.debug(f'New Spot Exclude List:\n{excluded=}')
        while True:
            new_x = random.randint(0, self.bound_x)
            new_y = random.randint(0, self.bound_y)
            if (new_x, new_y) not in excluded:
                self.x = new_x
                self.y = new_y
                break
        logging.info(f'New Food at ({new_x}, {new_y})')

class SnakeBody(SnakeObject):
    """This represents a piece of the snake which the player controls."""
    def __init__(self, spawn_x: int, spawn_y: int, char: str):
        super().__init__(spawn_x, spawn_y, char)
        # The last block will have next_block be None
        self.next_block: SnakeBody|None = None
        self.last_x: int = spawn_x
        self.last_y: int = spawn_y

    def set_position(self, new_x: int, new_y: int) -> None:
        self.last_x = self.x
        self.last_y = self.y
        self.x = new_x
        self.y = new_y

        if self.next_block:
            self.next_block.set_position(self.last_x, self.last_y)

    def grow(self) -> None:
        if not self.next_block:
            self.next_block = SnakeBody(self.last_x, self.last_y, self.char)
        else:
            self.next_block.grow()

    def __iter__(self):
        yield self
        next = self.next_block
        while next:
            yield next
            next = next.next_block

class SnakeHead(SnakeBody):
    def __init__(self, spawn_x: int, spawn_y: int, bound_x: int, bound_y: int, char: str) -> None:
        super().__init__(spawn_x, spawn_y, char)
        # Only the head block has a direction. Child blocks have direction set to None
        self.direction: Direction = Direction.RIGHT
        self.food: SnakeFood = SnakeFood(bound_x, bound_y, self.x, self.y)

        self.bound_x = bound_x
        self.bound_y = bound_y

    def update(self) -> None:
        logging.debug(f'x={self.x}, y={self.y} | {self.last_x=}, {self.last_y=}')
        match self.direction:
            case Direction.UP:
                self.set_position(self.x, self.y - 1)
            case Direction.DOWN:
                self.set_position(self.x, self.y + 1)
            case Direction.RIGHT:
                self.set_position(self.x + 1, self.y)
            case Direction.LEFT:
                self.set_position(self.x - 1, self.y)

        if self.collides_with(self.food):
            self.grow()
            places_food_cant_spawn = [
                (self.bound_x, self.bound_y)
            ]
            self.food.pick_new_spot(places_food_cant_spawn)

            if self.next_block:
                self.next_block.set_position(self.last_x, self.last_y)

    def change_direction(self, new_direction: Direction) -> bool:
        """Attempst to change the direction of the lead block."""
        veritcal_axis = (Direction.UP, Direction.DOWN)
        horizontal_axis = (Direction.LEFT, Direction.RIGHT)

        if self.direction in veritcal_axis and new_direction in veritcal_axis:
            return False

        if self.direction in horizontal_axis and new_direction in horizontal_axis:
            return False

        self.direction = new_direction
        logging.debug(f'Snake Head changed direction to {new_direction}')
        return True
