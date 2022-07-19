import typing

from .node import Node
from .context import Context


class Resolver(Node):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def resolve(self, text: str, context: Context) -> str:
        raise NotImplementedError("Can't use resolve on base Resolver class")

    def name(self) -> str:
        return super().name() + "-resolver"
