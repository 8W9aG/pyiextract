import argparse
import logging
import os
import typing
import urllib

import blink.main_dense as main_dense

from .context import Context
from .normaliser import Normaliser


class BlinkNormaliser(Normaliser):
    def __init__(self) -> None:
        super().__init__("BLINK")
        cache_folder = os.path.expanduser(os.path.join("~", ".blink"))
        os.makedirs(cache_folder, exist_ok=True)
        biencoder_model = "biencoder_wiki_large.bin"
        biencoder_config = "biencoder_wiki_large.json"
        entity_catalogue = "entity.jsonl"
        entity_encoding = "all_entities_large.t7"
        crossencoder_model = "crossencoder_wiki_large.bin"
        crossencoder_config = "crossencoder_wiki_large.json"
        faiss_hnsw_index = "faiss_hnsw_index.pkl"
        download_files = {
            f"http://dl.fbaipublicfiles.com/BLINK/{biencoder_model}",
            f"http://dl.fbaipublicfiles.com/BLINK/{biencoder_config}",
            f"http://dl.fbaipublicfiles.com/BLINK/{entity_catalogue}",
            f"http://dl.fbaipublicfiles.com/BLINK/{entity_encoding}",
            f"http://dl.fbaipublicfiles.com/BLINK/{crossencoder_model}",
            f"http://dl.fbaipublicfiles.com/BLINK/{crossencoder_config}",
            f"http://dl.fbaipublicfiles.com/BLINK/{faiss_hnsw_index}",
        }
        for download_file in download_files:
            parsed_url = urllib.parse.urlparse(download_file)
            filename = os.path.basename(parsed_url.path)
            download_path = os.path.join(cache_folder, filename)
            if os.path.exists(download_path):
                continue
            logging.info(f"Downloading {download_file} to {download_path}")
            urllib.request.urlretrieve(download_file, download_path)
        config = {
            "test_entities": None,
            "test_mentions": None,
            "interactive": False,
            "top_k": 1,
            "biencoder_model": os.path.join(cache_folder, biencoder_model),
            "biencoder_config": os.path.join(cache_folder, biencoder_config),
            "entity_catalogue": os.path.join(cache_folder, entity_catalogue),
            "entity_encoding": os.path.join(cache_folder, entity_encoding),
            "crossencoder_model": os.path.join(cache_folder, crossencoder_model),
            "crossencoder_config": os.path.join(cache_folder, crossencoder_config),
            "fast": True,
            "output_path": os.path.join(cache_folder, "logs"),
            "faiss_index": "hnsw",
            "index_path": os.path.join(cache_folder, faiss_hnsw_index),
        }
        self._args = argparse.Namespace(**config)
        self._models = main_dense.load_models(self._args, logger=None)
        self._valid_ent_types = {
            "PERSON",
            "NORP",
            "FAC",
            "ORG",
            "GPE",
            "LOC",
            "PRODUCT",
            "EVENT",
            "WORK_OF_ART",
            "LAW",
        }

    def normalise(self, text: str, context: Context) -> str:
        doc = context.resolved_doc()
        test_data: typing.List[typing.Dict] = []
        for ent in doc.ents:
            if not ent.has_extension("blink_id"):
                ent.set_extension("blink_id", default=None)
            if ent.label_ not in self._valid_ent_types:
                continue
            ent_str = str(ent)[:127]
            context_left = doc.text[: ent.start_char].lower()[-127:]
            context_right = doc.text[ent.end_char :].lower()[:127]
            test_data.append(
                {
                    "id": 0,
                    "label": "unknown",
                    "label_id": -1,
                    "context_left": context_left,
                    "mention": ent_str,
                    "context_right": context_right,
                    "ent": ent,
                }
            )
        if not test_data:
            return text
        _, _, _, _, _, predictions, scores, identifiers = main_dense.run(
            self._args, None, *self._models, test_data=test_data
        )
        for count, test_data_ent in enumerate(test_data):
            test_data_predictions = predictions[count]
            test_data_scores = scores[count]
            test_data_identifiers = identifiers[count]
            if test_data_predictions and test_data_scores and test_data_identifiers:
                if test_data_scores[0] > 325.0:
                    ent_str = str(test_data_ent["ent"])
                    logging.info(
                        f"Found entity ID {test_data_identifiers[0]} {test_data_predictions[0]} for {ent_str}"
                    )
                    test_data_ent["ent"]._.blink_id = test_data_identifiers[0]
        return text
