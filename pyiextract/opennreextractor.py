import typing

import opennre

from .extractor import Extractor
from .triple import Triple
from .spacy import NLP


class OpenNREExtractor(Extractor):
    def __init__(self):
        super().__init__()
        self._model = opennre.get_model('wiki80_bertentity_softmax')

    def extract(self, text: str) -> typing.List[Triple]:
        doc = NLP(text)
        # Find all the entities in a given sentence
        sentence_entities: typing.List[typing.List] = []
        unallocated_entities: typing.List = list(doc.ents)
        sentences = list(doc.sents)
        for sentence in sentences:
            current_entities = []
            for entity in unallocated_entities:
                if entity.start_char >= sentence.start_char and entity.end_char <= sentence.end_char:
                    current_entities.append(entity)
            for entity in current_entities:
                unallocated_entities.remove(entity)
            sentence_entities.append(current_entities)
        # Extract triples from the entities in a given sentence
        triples: typing.List[Triple] = []
        for count, sentence_entity_collection in enumerate(sentence_entities):
            sentence = str(sentences[count])
            for entity_count, sentence_entity in enumerate(sentence_entity_collection):
                for other_sentence_entity in sentence_entity_collection[entity_count + 1:]:
                    prediction = self._model.infer({
                        "text": sentence,
                        "h": {"pos": (sentence_entity.start_char, sentence_entity.end_char)},
                        "t": {"pos": (other_sentence_entity.start_char, other_sentence_entity.end_char)}
                    })
                    if prediction[1] > 0.5:
                        triples.append(Triple(str(sentence_entity), prediction[0], str(other_sentence_entity), "opennre"))
        return triples

    def name(self) -> str:
        return "opennre"
