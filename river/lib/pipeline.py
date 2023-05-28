from dataclasses import dataclass
from typing import Any, Dict, List
from threading import Thread

from .module import Module
from river.lib.helper.modes import ExecutionMode


@dataclass(kw_only=True)
class Pipeline(Module):
    host: str = "127.0.0.1"
    port: int = 9000

    def __post_init__(self):
        super().__post_init__()

    def enabled(self):
        return self.enabled

    def __call__(self, args: List = ..., kwargs: Dict = ...) -> Any:
        try:
            if self.mode is ExecutionMode.SEQUENTIAL:
                while self.enabled():
                    [component() for component in self.components.values()]
                    self.iterations += 1
            elif self.mode is ExecutionMode.THREADED:
                threads: List[Thread] = [Thread(target=self.threaded_function, args=[component]) for component in self.components.values()]
                [thread.start() for thread in threads]
                while self.enabled(): ...
                [thread.join() for thread in threads]
            elif self.mode is ExecutionMode.PROCESSED:
                raise ValueError("Processed mode is not yet implemented")
            else:
                raise ValueError(f"Unknown execution mode '{self.mode}'.")
        except KeyboardInterrupt:
            self.stop()
