from abc import ABC, abstractmethod


class NodeInput(ABC):
    @abstractmethod
    async def __anext__(self):
        pass

    def __aiter__(self):
        return self


class NodeOutput(ABC):

    @abstractmethod
    async def send(self, headers, data):
        pass
