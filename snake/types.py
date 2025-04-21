from enum import StrEnum
import curses
# Used by SnakeFood in pick_new_spot for readability 
type Coordinate = tuple[int, int]

class BoundingArea(tuple[int, int]):
    """Used by objects to track the playable area"""
    def contains_coordinate(self, coord: Coordinate) -> bool:
        bx, by = self
        cx, cy = coord

        return (cx >= 1 and cx <= bx-1 and cy >= 1 and cy <= by-1)

class GameObject:
    def update(self):
        return
    def draw(self, window: curses.window):
        raise NotImplementedError(window)
