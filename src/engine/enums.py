from enum import Enum, IntEnum

class MouseButton(IntEnum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3

class ButtonState(IntEnum):
    NORMAL = 1
    HOVER = 2
    ACTIVE = 3
