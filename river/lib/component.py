from dataclasses import dataclass, field
from typing import Any, Dict, List

from .pipes import Node


@dataclass(kw_only=True)
class Component:
    name: str = None
    description: str = ""
    nodes: Dict[str, Node] = field(default_factory=dict)
    iterations: int = field(init=False, default=0)

    def __post_init__(self):
        self.name = self.name if self.name is not None else self.__class__.__name__

    def __call__(self, args: List = [], kwargs: Dict = {}) -> Any: ...
