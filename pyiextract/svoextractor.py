import typing

from textacy import extract

from .extractor import Extractor
from .triple import Triple
from .context import Context


class SVOExtractor(Extractor):
    def __init__(self):
        super().__init__("svo")

    def extract(self, context: Context) -> typing.List[Triple]:
        return [self.create_triple(
            " ".join([str(x) for x in subject]),
            " ".join([str(x) for x in verb]),
            " ".join([str(x) for x in object]),
        ) for subject, verb, object in extract.subject_verb_object_triples(context.resolved_doc())]
