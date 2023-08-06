from ..creators import get_communicator_creator, get_node_creator
from ..configurations import ENV_VARIABLE_CONFIG

_COMMUNICATOR_CREATOR = get_communicator_creator(ENV_VARIABLE_CONFIG)

NODE = get_node_creator(ENV_VARIABLE_CONFIG).get_node_instance(
    node_input=_COMMUNICATOR_CREATOR.get_input_instance(),
    node_output=_COMMUNICATOR_CREATOR.get_output_instance(),
)
