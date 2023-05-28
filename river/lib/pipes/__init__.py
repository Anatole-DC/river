from .node import Node
from .buffer import Buffer

def set_link(entrypoint: Node, destination: Node) -> None:
    entrypoint.linked_nodes.append(destination)
