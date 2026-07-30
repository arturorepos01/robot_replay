from abc import ABC
from abc import abstractmethod


class BaseExecutor(ABC):

    @abstractmethod
    def execute(self, action, context):
        pass