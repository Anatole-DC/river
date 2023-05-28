from enum import Enum


class ExecutionMode(Enum):
    SEQUENTIAL: int = 0
    THREADED: int = 1
    PROCESSED: int = 2

class BufferStorageMode(Enum):
    FLOW: int = 0
    BUFF: int = 1
