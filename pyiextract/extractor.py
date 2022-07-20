import typing

from .triple import Triple
from .node import Node
from .context import Context


class Extractor(Node):
    def __init__(self, name: str):
        super().__init__(name)

    def extract(self, context: Context) -> typing.List[Triple]:
        raise NotImplementedError("Can't use extract on base Extractor class")

    def create_triple(
        self,
        head_entity: str,
        connection: str,
        tail_entity: str,
        doc: typing.Any,
        temporal: typing.Optional[str] = None,
        negated: bool = False,
        location: typing.Optional[str] = None) -> Triple:
        return Triple(
            head_entity,
            connection,
            tail_entity,
            doc,
            self.name(),
            temporal=temporal,
            negated=negated,
            location=location
        )

    def name(self) -> str:
        return super().name() + "-extractor"
