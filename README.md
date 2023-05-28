<h1 align="center">RIVER</h1>

_<h4 align="center">A library to manage data processing pipelines.</h4>_

River is a library to create and manage data processing pipelines.

## Summary

- [Summary](#summary)
- [Getting started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Setup](#setup)
- [Use the library](#use-the-library)
  - [Exemple](#exemple)
  - [Use River in projects](#use-river-in-projects)
  - [Create custom Components](#create-custom-components)

## Getting started

### Requirements

**[Poetry](https://python-poetry.org/)**

```bash
poetry --version
# Poetry (version 1.4.2)
```

**Python 3.10**

```bash
python3.10 --version
# Python 3.10.11
```

**Git**

```bash
git --version
# git version 2.25.1
```

### Installation

To get started, you must clone the repository.

```bash
git clone git@github.com:ocular-systems/river.git
```

### Setup

River comes with poetry, therefore you need to install the dependencies by running the following command.

```bash
poetry shell  # Create and activate a new virtual environment
poetry install
```

## Use the library

The library is focused around `Components` and `Nodes` to link those components together.

### Exemple

```python
from river import Pipeline, Module, Component, Node

ExemplePipeline = TestPipeline(
  components = {
      "FirstComponent": Component(),
      "AModule": Module(
          components = {
              "SecondComponent": Component(),
              "ThirdComponent": Component(),
          },
          nodes = {
              "input": Node(),
              "output": Node()
          },
          links=[
              (("nodes", "input"), ("SecondComponent", "input")),
              (("nodes", "input"), ("ThirdComponent", "input")),
              (("SecondComponent", "output"), ("nodes", "output")),
              (("ThirdComponent", "output"), ("nodes", "output")),
          ]

      ),
      "FourthComponent": Component()
  },

  links=[
      (("FirstComponent", "output"), ("AModule", "input")),
      (("AModule", "output"), ("FourthComponent", "input")),
  ]
)
```

Each link is a pair of tuple, each pointing to the component, and component's node that is to be involved in the link.

Modules are components that will contain a subset of components, and Pipelines are a subclass of Module. Modules manage their linkage inside themselves. In the exemple above, the "FourthComponent" cannot access the nodes inside "AModule".

### Use River in projects

To use river in projects, for now, you need to use the github url of the project to include it in your python's dependencies.

```bash
# With pip
pip install git+ssh://git@github.com:ocular-systems/river.git

# With poetry
poetry add git+ssh://git@github.com:ocular-systems/river.git
```

### Create custom Components

For complexe usecases, you can create your own components, modules or pipelines, by inheriting from those classes.

```python
from dataclasses import dataclass
from river import Component

@dataclass
class SuperComponent(Component):
  settings: Any = "Your settings"
  ...

  def __call__(self):
    # The execution code goes here
    ...
```

**Linkage**

To use nodes inside your custom components, you first need to define them in the `__post_init__` method (as dataclasses don't allow default dictionnaries).

```python
def __post_init__(self):
  super().__post_init__()
  self.nodes = {
    "name": Node()
  }
```

To fetch the values store in your nodes, you use the node's `get()` method.

To send a value to the pipeline, you use the `set()` method of the node.
