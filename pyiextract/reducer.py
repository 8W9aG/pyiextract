import typing

from .triple import Triple
from .node import Node
from .context import Context


class Reducer(Node):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def reduce(self, triples: typing.Set[Triple], context: Context) -> typing.Set[Triple]:
        raise NotImplementedError("Can't use reduce on base Reducer class")

    def name(self) -> str:
        return super().name() + "-reducer"
