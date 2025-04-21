import logging
from enum import IntEnum
from typing import NamedTuple
import json
import curses

curses_palette_color_map = {
    'black': curses.COLOR_BLACK,
    'white': curses.COLOR_WHITE,
    'green': curses.COLOR_GREEN,
    'red': curses.COLOR_RED,
    'blue': curses.COLOR_BLUE,
    'cyan': curses.COLOR_CYAN,
    'magenta': curses.COLOR_MAGENTA,
    'yellow': curses.COLOR_YELLOW
}

def map_color(color_name: str) -> int:
    return curses_palette_color_map[color_name]

class Color(IntEnum):
    PRIMARY = curses.color_pair(1)
    SECONDARY = curses.color_pair(2)
    TERTIARY = curses.color_pair(3)
    EMPTY = curses.color_pair(4)
    BORDER = curses.color_pair(5)

class ColorPair(NamedTuple):
    fg: int
    bg: int

    @classmethod
    def from_dict(cls, d: dict[str, str]) -> 'ColorPair':
        return cls(map_color(d['fg']), map_color(d['bg']))


class Palette(NamedTuple):
    name: str
    primary: ColorPair
    secondary: ColorPair
    tertiary: ColorPair
    empty: ColorPair
    border: ColorPair

    @classmethod
    def load_palettes_from_file(cls, file_path: str) -> dict[str, 'Palette']:
        with open(file_path) as f:
            palettes_json = json.load(f)

        palettes: dict[str, Palette] = {}

        for pj in palettes_json:
            name = pj['name']
            palettes[name] = Palette(
                name = name,
                primary = ColorPair.from_dict(pj['primary']),
                secondary = ColorPair.from_dict(pj['secondary']),
                tertiary = ColorPair.from_dict(pj['tertiary']),
                empty = ColorPair.from_dict(pj['empty']),
                border = ColorPair.from_dict(pj['border'])
            )

        return palettes

    def load_as_palette(self):
        curses.init_pair(1, self.primary.fg, self.primary.bg)
        curses.init_pair(2, self.secondary.fg, self.secondary.bg)
        curses.init_pair(3, self.tertiary.fg, self.tertiary.bg)
        curses.init_pair(4, self.empty.fg, self.empty.bg)
        curses.init_pair(5, self.border.fg, self.border.bg)

class ColorManager:
    def __init__(self, init_palette: str):
        self.palettes: dict[str, Palette] = Palette.load_palettes_from_file('data/palettes.json')
        self.set_palette(init_palette)
        logging.debug('Finished initializing colors')

    def set_palette(self, palette: str) -> None:
        self.palettes[palette].load_as_palette()


type ColorIfColorsEnabled = Color|None

