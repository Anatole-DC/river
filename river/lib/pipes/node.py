from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from river.lib.data import Data
from .buffer import Buffer


@dataclass
class Node:
    buffer: Buffer = field(init=False, default_factory=Buffer)
    linked_nodes: List[Node] = field(init=False, default_factory=list)

    def is_linked(self) -> bool:
        return len(self.linked_nodes) > 0

    def set(self, token: str, value: Data) -> None:
        if self.is_linked():
            [link.set(token, value) for link in self.linked_nodes]
        else:
            self.buffer.set(token, value)

    def get(self, token: str = None, default_value: Data = None) -> Data | None:
        value: Data = self.buffer.get(token)
        return value if value is not None else default_value
