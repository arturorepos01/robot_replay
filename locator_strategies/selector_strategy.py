from abc import ABC
from abc import abstractmethod


class SelectorStrategy(ABC):

    @abstractmethod
    def find(self, page, action):
        """
        Debe retornar:

            LocatorResult

        o

            None
        """
        pass