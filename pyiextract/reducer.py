import typing

from .triple import Triple


class Reducer:
    def __init__(self) -> None:
        pass

    def reduce(self, triples: typing.Set[Triple]) -> typing.Set[Triple]:
        raise NotImplementedError("Can't use reduce on base Reducer class")

    def name(self) -> str:
        return "reducer"
