from abc import ABC, abstractmethod


class Loader(ABC):
    @abstractmethod
    def put(self, news) -> None:
        pass