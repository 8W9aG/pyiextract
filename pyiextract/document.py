import typing

from .triple import Triple


class Document:
    def __init__(self) -> None:
        self._triples: typing.Dict[str, Triple] = {}

    def add_triple(self, triple: Triple) -> None:
        if triple in self._triples:
            self._triples[str(hash(triple))].add_extractors(triple.extractors())
        else:
            self._triples[str(hash(triple))] = triple

    def remove_triple(self, triple: Triple) -> None:
        del self._triples[str(hash(triple))]

    def triples(self, sort: bool = True) -> typing.List[Triple]:
        triples_list = list(self._triples.values())
        if sort:
            triples_list = sorted(
                triples_list, key=lambda x: len(x.extractors()), reverse=True
            )
        return triples_list
