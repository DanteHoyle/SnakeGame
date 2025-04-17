from enum import StrEnum, Enum, auto
from typing import NamedTuple

# Used by SnakeFood in pick_new_spot for readability 
type Coordinate = tuple[int, int]
# Used by objects to track the playable area
type BoundingArea = tuple[int, int]

class HeadDirection(StrEnum):
    UP = 'V'
    DOWN = 'Λ'
    LEFT = '>'
    RIGHT = '<'

class GameState(Enum):
    INIT = auto()
    GAMELOOP = auto()
    DEADSNAKE = auto()
    EXIT = auto()

class Config(NamedTuple):
    border_x: int = 80
    border_y: int = 60
    start_x: int = 10
    start_y: int = 10
    food_start_x: int = 30
    food_start_y: int = 20
    snake_head_char: str = "<"
    snake_body_char: str = '#'
    food_char: str = "@"
    frame_delay: float = 0.1
