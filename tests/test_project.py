from dataclasses import dataclass, field
from typing import Any, Dict, List
from pathlib import Path
from random import randint
import json
import unittest

from river import Pipeline, Component, Module, Node


@dataclass
class FileReaderComponent(Component):
    file: Path
    buffer: List[int] = field(init=False, default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self.nodes = {
            "pair": Node(),
            "impair": Node()
        }
        with open(self.file) as file:
            self.buffer = [int(number) for number in file]
            file.close()

    def __call__(self, args: List = ..., kwargs: Dict = ...) -> Any:
        if self.buffer == []: return

        number: int = self.buffer[0]
        if (number % 2) == 0:
            self.nodes["pair"].set(self.iterations, number)
        else:
            self.nodes["impair"].set(self.iterations, number)

        self.buffer.pop(0)

        self.iterations += 1

@dataclass
class FileWriterComponent(Component):
    file: Path

    def __post_init__(self):
        super().__post_init__()
        self.nodes = {
            "data": Node()
        }
        file = open(self.file, "w")
        file.write("{}")
        file.close()

    def __call__(self, args: List = ..., kwargs: Dict = ...) -> Any:
        data: str = self.nodes["data"].get()
        if data is None: return
        file = open(self.file)
        content = json.load(file)
        file.close()
        number, process = data.split("-")
        content[int(number)] = process
        file = open(self.file, "w")
        json.dump(content, file)
        file.close()

@dataclass
class NumberProcessingComponent(Component):
    label: str

    def __post_init__(self):
        super().__post_init__()
        self.nodes = {
            "number": Node(),
            "processed_number": Node()
        }

    def __call__(self, args: List = ..., kwargs: Dict = ...) -> Any:
        number = self.nodes["number"].get()
        if number is None: return
        self.nodes["processed_number"].set(randint(0, 10000), f"{number} - {self.label}")
        self.iterations += 1

@dataclass
class TestPipeline(Pipeline):
    def enabled(self):
        if self.iterations >= 10: self.stop()
        return self.enabled

TestPairImpairPipeline = TestPipeline(
    components = {
        "FileReaderComponent": FileReaderComponent(
            Path("tests/assets/numbers.txt")
        ),
        "NumberProcessingModule": Module(
            components = {
                "PairNumberComponent": NumberProcessingComponent("Pair", name="PairNumberComponent"),
                "ImpairNumberComponent": NumberProcessingComponent("Impair", name="ImpairNumberComponent"),
            },
            nodes = {
                "pair_input": Node(),
                "impair_input": Node(),
                "output": Node()
            },
            links=[
                (("nodes", "pair_input"), ("PairNumberComponent", "number")),
                (("nodes", "impair_input"), ("ImpairNumberComponent", "number")),
                (("PairNumberComponent", "processed_number"), ("nodes", "output")),
                (("ImpairNumberComponent", "processed_number"), ("nodes", "output")),
            ]

        ),
        "FileWriterComponent": FileWriterComponent(
            Path("assets/processed_numbers.json")
        )
    },

    links=[
        (("FileReaderComponent", "pair"), ("NumberProcessingModule", "pair_input")),
        (("FileReaderComponent", "impair"), ("NumberProcessingModule", "impair_input")),
        (("NumberProcessingModule", "output"), ("FileWriterComponent", "data")),
    ]
)

class TestRiverPipeline(unittest.TestCase):

    def test_project_output(self):
        TestPairImpairPipeline()
        result = json.load(open("tests/assets/processed_numbers.json"))
        self.assertEqual(result, {"1": " Impair", "2": " Pair", "3": " Impair", "4": " Pair", "5": " Impair", "6": " Pair", "7": " Impair", "8": " Pair", "9": " Impair", "10": " Pair"})
