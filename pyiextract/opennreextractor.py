import typing
import urllib
import os
import logging

import opennre

from .context import Context
from .extractor import Extractor
from .triple import Triple


class OpenNREExtractor(Extractor):
    def __init__(self):
        super().__init__("opennre")
        benchmark_folder = os.path.expanduser(os.path.join("~", ".opennre", "benchmark", "wiki80"))
        os.makedirs(benchmark_folder, exist_ok=True)
        download_path = os.path.join(benchmark_folder, "wiki80_rel2id.json")
        if not os.path.exists(download_path):
            download_file = "https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/benchmark/wiki80/wiki80_rel2id.json"
            logging.info(f"Downloading {download_file} to {download_path}")
            urllib.request.urlretrieve(download_file, download_path)
        pretrain_folder = os.path.expanduser(os.path.join("~", ".opennre", "pretrain", "bert-base-uncased"))
        os.makedirs(pretrain_folder, exist_ok=True)
        download_path = os.path.join(pretrain_folder, "config.json")
        if not os.path.exists(download_path):
            download_file = "https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/pretrain/bert-base-uncased/config.json"
            logging.info(f"Downloading {download_file} to {download_path}")
            urllib.request.urlretrieve(download_file, download_path)
        download_path = os.path.join(pretrain_folder, "pytorch_model.bin")
        if not os.path.exists(download_path):
            download_file = "https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/pretrain/bert-base-uncased/pytorch_model.bin"
            logging.info(f"Downloading {download_file} to {download_path}")
            urllib.request.urlretrieve(download_file, download_path)
        download_path = os.path.join(pretrain_folder, "vocab.txt")
        if not os.path.exists(download_path):
            download_file = "https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/pretrain/bert-base-uncased/vocab.txt"
            logging.info(f"Downloading {download_file} to {download_path}")
            urllib.request.urlretrieve(download_file, download_path)
        self._model = opennre.get_model("wiki80_bertentity_softmax")

    def extract(self, context: Context) -> typing.List[Triple]:
        doc = context.resolved_doc()
        # Find all the entities in a given sentence
        sentence_entities: typing.List[typing.List] = []
        unallocated_entities: typing.List = list(doc.ents)
        sentences = list(doc.sents)
        for sentence in sentences:
            current_entities = []
            for entity in unallocated_entities:
                if (
                    entity.start_char >= sentence.start_char
                    and entity.end_char <= sentence.end_char
                ):
                    current_entities.append(entity)
            for entity in current_entities:
                unallocated_entities.remove(entity)
            sentence_entities.append(current_entities)
        # Extract triples from the entities in a given sentence
        triples: typing.List[Triple] = []
        for count, sentence_entity_collection in enumerate(sentence_entities):
            spacy_sentence = sentences[count]
            sentence = str(spacy_sentence)
            for entity_count, sentence_entity in enumerate(sentence_entity_collection):
                for other_sentence_entity in sentence_entity_collection[
                    entity_count + 1 :
                ]:
                    prediction = self._model.infer(
                        {
                            "text": sentence,
                            "h": {
                                "pos": (
                                    sentence_entity.start_char,
                                    sentence_entity.end_char,
                                )
                            },
                            "t": {
                                "pos": (
                                    other_sentence_entity.start_char,
                                    other_sentence_entity.end_char,
                                )
                            },
                        }
                    )
                    if prediction[1] > 0.5:
                        triples.append(
                            self.create_triple(
                                str(sentence_entity),
                                prediction[0],
                                str(other_sentence_entity),
                                doc,
                            )
                        )
        return triples
