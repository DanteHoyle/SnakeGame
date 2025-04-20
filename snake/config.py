from typing import NamedTuple
import json

class Config(NamedTuple):
    border_x: int
    border_y: int
    start_x: int
    start_y: int
    food_start_x: int
    food_start_y: int
    snake_head_char: str
    snake_body_char: str
    food_char: str
    wall_char: str
    frame_delay: float

    @classmethod
    def from_config_file(cls, file_path: str) -> 'Config':
        with open(file_path, 'r') as f:
            cfg_json = json.load(f)
        return cls(
            border_x = cfg_json['border']['width'],
            border_y = cfg_json['border']['height'],
            start_x = cfg_json['snake']['start']['x'],
            start_y = cfg_json['snake']['start']['y'],
            snake_head_char = cfg_json['snake']['head_char'],
            snake_body_char = cfg_json['snake']['body_char'],
            food_start_x = cfg_json['food']['start']['y'],
            food_start_y = cfg_json['food']['start']['y'],
            food_char = cfg_json['food']['char'],
            wall_char = cfg_json['border']['char'],
            frame_delay = cfg_json['frame_delay'],
        )

