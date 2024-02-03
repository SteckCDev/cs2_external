from enum import Enum
from random import uniform


class Delay(float, Enum):
    ON_PAUSE = 1
    ON_ERROR = 2
    ITERATIONAL = 0.03
    TRIGGER_KEY_UNPRESSED = 0.1


class DynamicDelay:
    @staticmethod
    def before_trigger_button_press() -> float:
        return uniform(0.025, 0.035)

    @staticmethod
    def before_trigger_button_release() -> float:
        return uniform(0.035, 0.06)
