import typing

from .context import Context
from .reducer import Reducer
from .triple import Triple


class NERReducer(Reducer):
    def __init__(self) -> None:
        super().__init__("ner")

    def reduce(
        self, triples: typing.Set[Triple], context: Context
    ) -> typing.Set[Triple]:
        entities = {str(x).lower() for x in context.resolved_doc().ents}
        return {
            x
            for x in triples
            if x.head_entity().name().lower() in entities
            or x.tail_entity().name().lower() in entities
        }
