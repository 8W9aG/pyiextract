import typing

from .entity import Entity


class Triple:
    def __init__(
        self,
        head_entity: str,
        connection: str,
        tail_entity: str,
        doc: typing.Any,
        extractor: str,
        temporal: typing.Optional[str] = None,
        negated: bool = False,
        location: typing.Optional[str] = None,
        is_quote: bool = False,
    ) -> None:
        entities = {str(x): x for x in doc.ents}
        head_entity_id = head_entity
        if head_entity in entities:
            if entities[head_entity]._.blink_id is not None:
                head_entity_id = entities[head_entity]._.blink_id
        tail_entity_id = tail_entity
        if tail_entity in entities:
            if entities[tail_entity]._.blink_id is not None:
                tail_entity_id = entities[tail_entity]._.blink_id
        self._head_entity = Entity(str(head_entity), head_entity_id)
        self._connection = connection
        self._tail_entity = Entity(str(tail_entity), tail_entity_id)
        self._temporal = temporal
        self._negated = negated
        self._location = location
        self._is_quote = is_quote
        self._extractors = {extractor}

    def head_entity(self) -> Entity:
        return self._head_entity

    def connection(self) -> str:
        return self._connection

    def tail_entity(self) -> Entity:
        return self._tail_entity

    def temporal(self) -> typing.Optional[str]:
        return self._temporal

    def negated(self) -> bool:
        return self._negated

    def location(self) -> typing.Optional[str]:
        return self._location

    def extractors(self) -> typing.Set[str]:
        return self._extractors

    def add_extractor(self, extractor: str) -> None:
        self._extractors.add(extractor)

    def add_extractors(self, extractors: typing.Set[str]) -> None:
        self._extractors |= extractors

    def _base_str(self) -> str:
        return f"{str(self._head_entity)} -> {self._connection} -> {str(self._tail_entity)}"

    def __str__(self) -> str:
        output = ""
        if self._negated:
            output += "[NEGATED] "
        if self._is_quote:
            output += "[QUOTE] "
        output += self._base_str()
        if self._temporal is not None:
            output += f" in {self._temporal}"
        if self._location is not None:
            output += f" at {self._location}"
        output += " {" + ",".join(self._extractors) + "}"
        return output

    def __hash__(self) -> int:
        return hash(self._base_str())
