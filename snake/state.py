import logging
from enum import StrEnum

class Status(StrEnum):
    INIT = 'Initialization'
    GAMELOOP = 'Game Loop'
    DEADSNAKE = 'Dead Snake'
    EXIT = 'Exiting'

class SharedGameState:
    def __init__(self):
        self.state: Status = Status.INIT
        self.score: int = 0
