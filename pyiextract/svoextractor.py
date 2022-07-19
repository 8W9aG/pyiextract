import typing

from textacy import extract

from .extractor import Extractor
from .triple import Triple
from .spacy import NLP


class SVOExtractor(Extractor):
    def __init__(self):
        super().__init__()

    def extract(self, text: str) -> typing.List[Triple]:
        return [Triple(
            " ".join([str(x) for x in subject]),
            " ".join([str(x) for x in verb]),
            " ".join([str(x) for x in object]),
            "svo",
        ) for subject, verb, object in extract.subject_verb_object_triples(NLP(text))]

    def name(self) -> str:
        return "svo"
