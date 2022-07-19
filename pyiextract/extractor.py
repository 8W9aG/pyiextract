import typing

from .triple import Triple


class Extractor:
    def __init__(self):
        pass

    def extract(self, text: str) -> typing.List[Triple]:
        raise NotImplementedError("Can't use extract on base Extractor class")

    def name(self) -> str:
        return "base"
