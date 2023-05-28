from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List
from random import randint

from river import Pipeline, Module, Component, Node, ExecutionMode
from river.lib.data import Data


@dataclass
class RandomValueData:
    number: int

@dataclass
class RandomValueComponent(Component):
    def __post_init__(self):
        super().__post_init__()
        self.nodes = {
            "number": Node()
        }

    def __call__(self, args: List = ..., kwargs: Dict = ...) -> Any:
        random_number = randint(0, 10)
        print(f"{self.name} : {random_number}")
        self.nodes["number"].set(str(self.iterations), RandomValueData(random_number))
        self.iterations += 1

@dataclass
class PrintData(Component):
    def __post_init__(self):
        super().__post_init__()
        self.nodes = {
            "data": Node()
        }

    def __call__(self, args: List = ..., kwargs: Dict = ...) -> Any:
        value: Data = self.nodes["data"].get()
        if value is None: return
        print(f"{self.name} : {value=}")

simple_pipeline = Pipeline(
    name="PipelineWithValues",
    mode=ExecutionMode.THREADED,
    components={
        "RandomValueModule": Module(
            components={
                "random1": RandomValueComponent(name="Random1"),
            },
            nodes={
                "random_output1": Node(),
            },
            links=[
                (("random1", "number"), ("nodes", "random_output1")),
            ]
        ),
        "PrintDataComponent": PrintData(),
    },
    links=[
        (("RandomValueModule", "random_output1"), ("PrintDataComponent", "data")),
    ]
)

def main():
    simple_pipeline()

if __name__ == "__main__":
    main()
