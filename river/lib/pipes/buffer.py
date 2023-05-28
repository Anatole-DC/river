from dataclasses import dataclass, field, KW_ONLY
from typing import Dict, Type, Any

from river.lib.data import Data
from river.lib.helper.modes import BufferStorageMode


@dataclass
class Buffer:
    mode: BufferStorageMode = BufferStorageMode.BUFF
    data_type: Type = Any
    STORAGE: Dict[str, Data] = field(init=False, default_factory=dict)
    _: KW_ONLY
    label: str = None

    def set(self, token: str, value: Data):
        if self.mode is BufferStorageMode.FLOW:
            self.STORAGE[token] = value
        elif self.mode is BufferStorageMode.BUFF:
            self.STORAGE[token] = value
        else:
            raise NotImplementedError(f"Buffer storage mode {self.mode} not implemented")

    def get(self, token: str = None) -> Data | None:
        if self.STORAGE == {}:
            return

        if  token is not None and token not in self.STORAGE.keys():
            return

        key: str = token if token is not None else list(self.STORAGE.keys())[0]
        value: Data = self.STORAGE[key]
        self.STORAGE.pop(key)

        return value
