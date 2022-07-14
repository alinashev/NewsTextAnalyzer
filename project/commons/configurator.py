from abc import ABC, abstractmethod
from typing import Any


class Configurator(ABC):

    @abstractmethod
    def get_date(self) -> Any:
        pass
