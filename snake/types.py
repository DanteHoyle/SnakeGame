from enum import StrEnum
from typing import NamedTuple
import curses

# Used by SnakeFood in pick_new_spot for readability 
type Coordinate = tuple[int, int]

class BoundingArea(tuple[int, int]):
    """Used by objects to track the playable area"""
    def contains_coordinate(self, coord: Coordinate) -> bool:
        bx, by = self
        cx, cy = coord

        return (cx >= 1 and cx <= bx-1 and cy >= 1 and cy <= by-1)

class HeadDirection(StrEnum):
    UP = 'V'
    DOWN = 'Λ'
    LEFT = '>'
    RIGHT = '<'

class States(StrEnum):
    INIT = 'Initialization'
    GAMELOOP = 'Game Loop'
    DEADSNAKE = 'Dead Snake'
    EXIT = 'Exiting'

class Config(NamedTuple):
    border_x: int = 30
    border_y: int = 15
    start_x: int = 10
    start_y: int = 10
    food_start_x: int = 30
    food_start_y: int = 20
    snake_head_char: str = '<'
    snake_body_char: str = '#'
    food_char: str = '@'
    wall_char: str = '='
    frame_delay: float = 0.1

class GameObject:
    def update(self):
        return
    def draw(self, window: curses.window):
        raise NotImplementedError(window)
