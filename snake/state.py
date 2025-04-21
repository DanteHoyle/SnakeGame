from enum import StrEnum
import logging

class Status(StrEnum):
    INIT = 'Initialization'
    GAMELOOP = 'Game Loop'
    DEADSNAKE = 'Dead Snake'
    EXIT = 'Exiting'

class SharedGameState:
    def __init__(self):
        self._state: Status = Status.INIT
        self.score: int = 0

    @property
    def state(self) -> Status:
        return self._state

    @state.setter
    def state(self, new_state: Status):
        logging.info(f'Old State "{self._state.value}" -> New State {new_state.value}')
        self._state = new_state
