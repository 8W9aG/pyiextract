import typing


class Triple:
    def __init__(
        self,
        head_entity: str,
        connection: str,
        tail_entity: str,
        extractor: str,
        temporal: typing.Optional[str] = None,
        negated: bool = False,
        location: typing.Optional[str] = None) -> None:
        self._head_entity = head_entity
        self._connection = connection
        self._tail_entity = tail_entity
        self._temporal = temporal
        self._negated = negated
        self._location = location
        self._extractors = {extractor}

    def head_entity(self) -> str:
        return self._head_entity

    def connection(self) -> str:
        return self._connection

    def tail_entity(self) -> str:
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

    def _base_str(self) -> str:
        return f"{self._head_entity} -> {self._connection} -> {self._tail_entity}"

    def __str__(self) -> str:
        output = ""
        if self._negated:
            output += "[NEGATED] "
        output += self._base_str()
        if self._temporal is not None:
            output += f" in {self._temporal}"
        if self._location is not None:
            output += f" at {self._location}"
        output += " {" + ",".join(self._extractors) + "}"
        return output

    def __hash__(self) -> int:
        return hash(self._base_str())
