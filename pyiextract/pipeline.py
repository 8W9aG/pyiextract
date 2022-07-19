import typing

from .resolver import Resolver
from .extractor import Extractor
from .triple import Triple
from .reducer import Reducer
from .document import Document


class Pipeline:
    def __init__(self, resolvers: typing.List[Resolver], extractors: typing.List[Extractor], reducers: typing.List[Reducer]) -> None:
        self._resolvers = resolvers
        self._extractors = extractors
        self._reducers = reducers

    def extract(self, text: str) -> Document:
        document = Document()
        for resolver in self._resolvers:
            text = resolver.resolve(text)
        for extractor in self._extractors:
            for triple in extractor.extract(text):
                document.add_triple(triple)
        for reducer in self._reducers:
            triples = set(document.triples(sort=False))
            reduced_triples = reducer.reduce(triples)
            for triple in triples.difference(reduced_triples):
                document.remove_triple(triple)
        return document

    def name(self) -> str:
        return "base"
