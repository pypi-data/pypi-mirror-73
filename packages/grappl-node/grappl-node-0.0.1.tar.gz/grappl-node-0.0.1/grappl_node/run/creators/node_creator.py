from ...core.communication import NodeOutput, NodeInput
from ...core.node import Node
from dataclasses import dataclass


@dataclass
class NodeCreator:
    node_class_module: str
    node_class_name: str
    node_class_arguments: str

    def get_node_instance(self, node_input: NodeInput, node_output: NodeOutput) -> Node:
        return getattr(__import__(self.node_class_module), self.node_class_name)(
            node_input=node_input,
            node_output=node_output,
            **self.node_class_arguments
        )
