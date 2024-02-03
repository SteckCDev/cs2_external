import logging
from threading import Thread

from misc.exceptions import DaemonsDeadError, DaemonsIsRunningError

from .abstract_unit import AbstractUnit


logger = logging.getLogger(__name__)


class UnitManager:
    def __init__(self, units: list[AbstractUnit]) -> None:
        self.__daemons_state: bool | None = None

        self.__units: list[AbstractUnit] = units
        self.__units_threads: list[Thread] = [
            Thread(name=str(unit), target=unit.daemon, daemon=True) for unit in self.__units
        ]

    def start_daemons(self) -> None:
        if self.__daemons_state is not None:
            raise DaemonsIsRunningError("Daemons based on threads and designed to be started only once")

        logger.info("Starting daemons")

        for thread in self.__units_threads:
            thread.start()

    def pause_daemons_if_running(self) -> None:
        if self.__daemons_state is None:
            raise DaemonsDeadError("Start daemons first")

        if not self.__daemons_state:
            return

        logger.info("Pausing daemons")

        for unit in self.__units:
            unit.set_state(new_state=False)

    def launch_daemons_if_paused(self) -> None:
        if self.__daemons_state is None:
            raise DaemonsDeadError("Start daemons first")

        if self.__daemons_state:
            return

        logger.info("Launching daemons")

        for unit in self.__units:
            unit.set_state(new_state=True)
