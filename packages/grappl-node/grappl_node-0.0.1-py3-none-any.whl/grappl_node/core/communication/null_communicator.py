from .base_communicator import NodeInput, NodeOutput


class NullNodeInput(NodeInput):
    async def __anext__(self):
        return None


class NullNodeOutput(NodeOutput):
    async def send(self):
        pass
