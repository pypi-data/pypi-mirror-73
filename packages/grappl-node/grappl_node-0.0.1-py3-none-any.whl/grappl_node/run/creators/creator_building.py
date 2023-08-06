from inspect import signature
from .communicator_creator import CommunicatorCreator
from .node_creator import NodeCreator


def init_class_with_required_arguments(cls, all_arguments: dict):
    return cls(**{key: all_arguments[key] for key in signature(cls).parameters})


def get_communicator_creator(configuration_parameters: dict) -> CommunicatorCreator:
    return init_class_with_required_arguments(CommunicatorCreator, configuration_parameters)


def get_node_creator(configuration_parameters: dict) -> NodeCreator:
    return init_class_with_required_arguments(NodeCreator, configuration_parameters)
