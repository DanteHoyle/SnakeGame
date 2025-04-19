import logging

from snake.types import States

class GameState:
    def __init__(self):
        self.state: States = States.INIT

    def __eq__(self, value: object) -> bool:
        return self.state == value

    def __str__(self) -> str:
        return self.state.value

    def set_state(self, state: States):
        current_state = self.state
        self.state = state
        logging.info(f'Game State [{current_state.value}] -> [{self.state.value}]')

    def enter_gameloop(self):
        self.set_state(States.GAMELOOP)

    def enter_deadsnake(self):
        self.set_state(States.DEADSNAKE)

    def enter_exit(self):
        self.set_state(States.EXIT)

    def reset(self):
        self.set_state(States.INIT)
