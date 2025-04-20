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

def color(color_name: str) -> int:
    return curses_palette_color_map[color_name]

class Color(IntEnum):
    PRIMARY = curses.color_pair(1)
    SECONDARY = curses.color_pair(2)
    EMPTY = curses.color_pair(3)
    BORDER = curses.color_pair(4)

class ColorPair(NamedTuple):
    fg: int
    bg: int

    @classmethod
    def from_dict(cls, d: dict[str, str]) -> 'ColorPair':
        return cls(color(d['fg']), color(d['bg']))


class Palette(NamedTuple):
    name: str
    primary: ColorPair
    secondary: ColorPair
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
                empty = ColorPair.from_dict(pj['empty']),
                border = ColorPair.from_dict(pj['border'])
            )

        return palettes

class ColorManager:
    def __init__(self):
        self.palettes: dict[str, Palette] = Palette.load_palettes_from_file('data/palettes.json')
        self.current_palette = 'default'
        self.set_palette(self.current_palette)
        logging.debug('Finished initializing colors')

    def set_palette(self, palette: str) -> None:
        p = self.palettes[palette]

        curses.init_pair(1, p.primary.fg, p.primary.bg)
        curses.init_pair(2, p.secondary.fg, p.secondary.bg)
        curses.init_pair(3, p.empty.fg, p.empty.bg)
        curses.init_pair(4, p.border.fg, p.border.bg)
        logging.info(f'Color Palette Set To {palette}')

type ColorIfColorsEnabled = Color|None

