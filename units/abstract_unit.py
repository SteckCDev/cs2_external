from abc import ABC, abstractmethod


class AbstractUnit(ABC):
    @abstractmethod
    def set_state(self, new_state: bool) -> None:
        ...

    @abstractmethod
    def daemon(self) -> None:
        ...
