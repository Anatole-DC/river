from dataclasses import dataclass

from .buffer import Buffer

@dataclass
class Input:

    def is_linked(self) -> bool:
        return self.link is not None