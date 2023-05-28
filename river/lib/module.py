from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Callable
from threading import Thread

from river.lib.pipes import Node, set_link
from river.lib.helper.modes import ExecutionMode
from river.lib.errors import NodeNameError
from .component import Component


@dataclass(kw_only=True)
class Module(Component):
    components: Dict[str, Component]
    nodes: Dict[str, Node] = field(default_factory=dict)
    mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    links: List[Tuple[Tuple[str, str], Tuple[str, str]]] = field(default_factory=list)
    enabled: True = field(init=False, default=True)
    buffers: List = field(init=False, default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self.set_links()

    def __call__(self, args: List = [], kwargs: Dict = {}) -> Any:
        if self.mode is ExecutionMode.SEQUENTIAL:
            [component() for component in self.components.values()]
        elif self.mode is ExecutionMode.THREADED:
            threads: List[Thread] = [Thread(target=self.threaded_function, args=[component]) for component in self.components.values()]
            [thread.start() for thread in threads]
            try:
                while self.enabled: ...
            except KeyboardInterrupt:
                self.stop()
            [thread.join() for thread in threads]
        elif self.mode is ExecutionMode.PROCESSED:
            raise ValueError("Processed mode is not yet implemented")
        else:
            raise ValueError(f"Unknown execution mode '{self.mode}'.")

    def stop(self):
        print(f"Stopping {self.name}")
        self.enabled = False
        [module.stop() for module in self.components.values() if isinstance(module, Module)]

    def threaded_function(self, function : Callable):
        while self.enabled: function()

    def set_links(self):
        for link in self.links:
            (entrypoint, entrypoint_key), (destination, destination_key)= link

            try:
                entrypoint_node: Node = self.components[entrypoint].nodes[entrypoint_key] if entrypoint != "nodes" else self.nodes[entrypoint_key]
            except KeyError as wrong_key:
                raise NodeNameError(f"In {self.name}, entrypoint {entrypoint}, wrong key {wrong_key}")

            try:
                destination_node: Node = self.components[destination].nodes[destination_key] if destination != "nodes" else self.nodes[destination_key]
            except KeyError as wrong_key:
                raise NodeNameError(f"In {self.name}, destination {destination}, key {wrong_key}")

            print(f"Set link between {entrypoint}'s {entrypoint_key} and {destination}'s {destination_key}")
            self.buffers.append(set_link(entrypoint_node, destination_node))
