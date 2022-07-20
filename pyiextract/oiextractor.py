import typing

from allennlp.predictors.predictor import Predictor

from .context import Context
from .extractor import Extractor
from .strfind import extract_entities_span
from .triple import Triple


class OIExtractor(Extractor):
    def __init__(self):
        super().__init__("openie")
        self._predictor = Predictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/openie-model.2020.03.26.tar.gz"
        )

    def extract(self, context: Context) -> typing.List[Triple]:
        triples: typing.List[Triple] = []
        doc = context.resolved_doc()
        for sent in doc.sents:
            prediction = self._predictor.predict(sentence=str(sent))
            words = prediction["words"]
            for verb in prediction["verbs"]:
                head_entity_words = []
                tail_entity_words = []
                connection_words = []
                temporal_words = []
                negated_words = []
                location_words = []
                for count, tag in enumerate(verb["tags"]):
                    word = words[count]
                    if tag.endswith("-ARG0"):
                        head_entity_words.append(word)
                    elif tag.endswith("-V"):
                        connection_words.append(word)
                    elif tag.endswith("-ARG1"):
                        tail_entity_words.append(word)
                    elif tag.endswith("ARGM-TMP"):
                        temporal_words.append(word)
                    elif tag.endswith("ARGM-NEG"):
                        negated_words.append(word)
                    elif tag.endswith("ARGM-LOC"):
                        location_words.append(word)
                if head_entity_words and tail_entity_words and connection_words:
                    head_entity_text = " ".join(head_entity_words)
                    tail_entity_text = " ".join(tail_entity_words)
                    relation_text = " ".join(connection_words)
                    triples.append(
                        self.create_triple(
                            head_entity_text,
                            relation_text,
                            tail_entity_text,
                            doc,
                            temporal=None
                            if not temporal_words
                            else " ".join(temporal_words),
                            negated=False if not negated_words else True,
                            location=None
                            if not location_words
                            else " ".join(location_words),
                        )
                    )
        return triples
