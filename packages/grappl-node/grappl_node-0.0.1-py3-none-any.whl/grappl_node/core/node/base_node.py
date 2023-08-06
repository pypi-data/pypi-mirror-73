from abc import ABC, abstractmethod
from dataclasses import dataclass
from ..communication.base_communicator import NodeOutput, NodeInput


@dataclass
class Node(ABC):
    """
    Class that specifies the interface for creating a node.
    """
    node_input: NodeInput
    node_output: NodeOutput

    @abstractmethod
    async def run(self):
        pass
