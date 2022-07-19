import typing

from .reducer import Reducer
from .triple import Triple


class CoreferenceReducer(Reducer):
    def __init__(self) -> None:
        super().__init__()
        self._bad_entities = {"he", "him", "she", "her", "they", "them"}

    def reduce(self, triples: typing.Set[Triple]) -> typing.Set[Triple]:
        return {x for x in triples if x.head_entity().lower() not in self._bad_entities and x.tail_entity().lower() not in self._bad_entities}
