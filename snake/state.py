from enum import StrEnum
import logging

class Status(StrEnum):
    INIT = 'Initialization'
    SETUPGAME = 'Setting Up the Game'
    WAITTOSTART = 'Waiting to start'
    GAMELOOP = 'Game Loop'
    DEADSNAKE = 'Dead Snake'
    SHOWSCORE = 'Show Score'
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
        logging.info(f'State is changing: "{self._state.value}" -> "{new_state.value}"')
        self._state = new_state
