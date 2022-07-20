import typing

from .context import Context
from .pronouns import PRONOUNS
from .reducer import Reducer
from .triple import Triple


class CoreferenceReducer(Reducer):
    def __init__(self) -> None:
        super().__init__("coreference")

    def reduce(
        self, triples: typing.Set[Triple], context: Context
    ) -> typing.Set[Triple]:
        return {
            x
            for x in triples
            if x.head_entity().name().lower() not in PRONOUNS
            and x.tail_entity().name().lower() not in PRONOUNS
        }
