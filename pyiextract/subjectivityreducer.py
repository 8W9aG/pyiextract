import typing

from textblob import TextBlob

from .context import Context
from .reducer import Reducer
from .triple import Triple


class SubjectivityReducer(Reducer):
    def __init__(self) -> None:
        super().__init__("subjectivity")

    def reduce(
        self, triples: typing.Set[Triple], context: Context
    ) -> typing.Set[Triple]:
        new_triples: typing.Set[Triple] = set()
        for triple in triples:
            triple_str = str(triple).replace(" ->", "")
            blob = TextBlob(triple_str)
            if blob.sentiment.subjectivity > 0.5:
                continue
            new_triples.add(triple)
        return new_triples
