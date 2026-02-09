from enum import Enum, auto

class SystemState(Enum):
    """
    System states for gesture control.
    Based on Om's implementation.
    """
    OFF = auto()       # Mouse control disabled
    ON = auto()        # Mouse control enabled
    FROZEN = auto()    # Cursor frozen in place
    PAUSED = auto()    # Face lost / system paused
