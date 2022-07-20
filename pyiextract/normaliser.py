from .context import Context
from .node import Node


class Normaliser(Node):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def normalise(self, text: str, context: Context) -> str:
        raise NotImplementedError("Can't use normalise on base Normaliser class")

    def name(self) -> str:
        return super().name() + "-normaliser"
