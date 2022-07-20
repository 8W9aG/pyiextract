import logging
import typing

from .context import Context
from .document import Document
from .extractor import Extractor
from .normaliser import Normaliser
from .reducer import Reducer


class Pipeline:
    def __init__(
        self,
        normalisers: typing.List[Normaliser],
        extractors: typing.List[Extractor],
        reducers: typing.List[Reducer],
    ) -> None:
        self._normalisers = normalisers
        self._extractors = extractors
        self._reducers = reducers

    def extract(self, text: str) -> Document:
        logging.info(f"Extract from text: {text}")
        document = Document()
        context = Context(text)
        for normaliser in self._normalisers:
            new_text = normaliser.normalise(text, context)
            if new_text != text:
                text = new_text
                context.set_resolved_text(text)
                logging.info(f"Normalised text from {normaliser.name()}: {text}")
        for extractor in self._extractors:
            for triple in extractor.extract(context):
                document.add_triple(triple)
                logging.info(f"Found triple from {extractor.name()}: {str(triple)}")
        for reducer in self._reducers:
            triples = set(document.triples(sort=False))
            reduced_triples = reducer.reduce(triples, context)
            for triple in triples.difference(reduced_triples):
                logging.info(f"Removed triple from {reducer.name()}: {str(triple)}")
                document.remove_triple(triple)
        return document
