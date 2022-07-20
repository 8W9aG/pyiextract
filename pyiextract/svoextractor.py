import typing

from textacy import extract

from .context import Context
from .extractor import Extractor
from .triple import Triple


class SVOExtractor(Extractor):
    def __init__(self):
        super().__init__("svo")

    def extract(self, context: Context) -> typing.List[Triple]:
        doc = context.resolved_doc()
        triples = [
            self.create_triple(
                " ".join([str(x) for x in subject]),
                " ".join([str(x) for x in verb]),
                " ".join([str(x) for x in object]),
                doc,
            )
            for subject, verb, object in extract.subject_verb_object_triples(doc)
        ]
        triples.extend(
            [
                self.create_triple(
                    " ".join([str(x) for x in speaker]),
                    " ".join([str(x) for x in cue]),
                    " ".join([str(x) for x in content]),
                    doc,
                    is_quote=True,
                )
                for speaker, cue, content in extract.direct_quotations(doc)
            ]
        )
        return triples
