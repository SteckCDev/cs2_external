import logging
from time import sleep
from typing import Final

import pymem
from win32.win32gui import GetForegroundWindow, GetWindowText

from units import TriggerUnit, UnitManager


PROCESS_NAME: Final[str] = "cs2.exe"
CLIENT_MODULE_NAME: Final[str] = "client.dll"
WINDOW_NAME: Final[str] = "Counter-Strike 2"

logger = logging.getLogger(__name__)

pm = pymem.Pymem(PROCESS_NAME)
client: int = pymem.process.module_from_name(pm.process_handle, CLIENT_MODULE_NAME).lpBaseOfDll

unit_manager = UnitManager(
    units=[
        TriggerUnit(pm=pm, client=client),
    ]
)


def main() -> None:
    logger.info("Starting up")

    unit_manager.start_daemons()

    while True:
        try:
            if GetWindowText(GetForegroundWindow()) != WINDOW_NAME:
                unit_manager.pause_daemons_if_running()
            else:
                unit_manager.launch_daemons_if_paused()

            sleep(3)

        except KeyboardInterrupt:
            logger.info("Shutting down")
            break


if __name__ == "__main__":
    main()
