

class Entity:
    def __init__(self, name: str, identifier: str) -> None:
        self._name = name
        self._identifier = identifier

    def name(self) -> str:
        return self._name

    def identifier(self) -> str:
        return self._identifier

    def __hash__(self) -> int:
        return hash(self._identifier)

    def __str__(self) -> str:
        output = self._name
        if self._identifier != self._name:
            output += f" ({self._identifier})"
        return output
