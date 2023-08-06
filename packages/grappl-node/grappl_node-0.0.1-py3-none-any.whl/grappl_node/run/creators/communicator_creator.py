from ...core.communication.base_communicator import NodeOutput, NodeInput
from dataclasses import dataclass


@dataclass
class CommunicatorCreator:
    input_class_module: str
    output_class_module: str
    input_class_name: str
    output_class_name: str
    input_arguments: dict
    output_arguments: dict

    def get_input_instance(self) -> NodeInput:
        module = __import__(self.input_class_module)
        return getattr(module, self.input_class_name)(**self.input_arguments)

    def get_output_instance(self) -> NodeOutput:
        module = __import__(self.output_class_module)
        return getattr(module, self.output_class_name)(**self.output_arguments)
