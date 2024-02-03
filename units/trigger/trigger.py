import logging
from time import sleep
from typing import Final

import keyboard
from pymem import Pymem
from pynput.mouse import Button, Controller

from memory import Offset
from units.abstract_unit import AbstractUnit

from .delays import Delay, DynamicDelay


TRIGGER_KEY: Final[str] = "alt"

logger = logging.getLogger(__name__)


class TriggerUnit(AbstractUnit):
    def __init__(self, pm: Pymem, client: int):
        self.__pm: Pymem = pm
        self.__client: int = client
        self.__mouse: Controller = Controller()

        self.__state = True

    def set_state(self, new_state: bool) -> None:
        self.__state = new_state

        logger.info("Daemon launched" if self.__state else "Daemon paused")

    def __crosshair_on_target(self) -> bool:
        player = self.__pm.read_longlong(self.__client + Offset.dw_local_player_pawn)

        if (entity_id := self.__pm.read_int(player + Offset.m_i_id_ent_index)) <= 0:
            return False

        entity_list = self.__pm.read_longlong(self.__client + Offset.dw_entity_list)

        entity_entry = self.__pm.read_longlong(
            entity_list + 0x8 * (entity_id >> 9) + 0x10
        )

        entity = self.__pm.read_longlong(
            entity_entry + 120 * (entity_id & 0x1FF)
        )

        entity_hp = self.__pm.read_int(entity + Offset.m_i_health)

        if entity_hp <= 0:
            return False

        entity_team = self.__pm.read_int(entity + Offset.m_i_team_num)
        player_team = self.__pm.read_int(player + Offset.m_i_team_num)

        if entity_team == player_team:
            return False

        return True

    def __emulate_fire(self) -> None:
        sleep(DynamicDelay.before_trigger_button_press())
        self.__mouse.press(Button.left)
        sleep(DynamicDelay.before_trigger_button_release())
        self.__mouse.release(Button.left)

    def daemon(self) -> None:
        logger.info("Starting daemon")

        while True:
            while self.__state:
                # noinspection PyBroadException
                try:
                    if not keyboard.is_pressed(TRIGGER_KEY):
                        sleep(Delay.TRIGGER_KEY_UNPRESSED)
                        continue

                    if not self.__crosshair_on_target():
                        continue

                    self.__emulate_fire()

                    sleep(Delay.ITERATIONAL)

                except Exception:
                    logger.exception("Exception encountered on iteration")
                    sleep(Delay.ON_ERROR)

            sleep(Delay.ON_PAUSE)

    def __repr__(self) -> str:
        return "trigger_unit"
