import enum


class STATE_GAME(enum.Enum):
    CANCEL = 'CANCEL'
    EXIT = 'EXIT'
    JOIN = 'JOIN'
    PRESENTATION = 'PRESENTATION'
    START = 'START'
    WAIT = 'WAIT'
    PLAY = 'PLAY'
    END = 'END'
    READY = 'READY'
    TIME = 'TIME'
    END_RACE = 'END_RACE'
