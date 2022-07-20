from .node import Node
from .context import Context


class Normaliser(Node):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def normalise(self, text: str, context: Context) -> str:
        raise NotImplementedError("Can't use normalise on base Normaliser class")

    def name(self) -> str:
        return super().name() + "-normaliser"
