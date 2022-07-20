import typing

from allennlp.predictors.predictor import Predictor

from .context import Context
from .normaliser import Normaliser

"""
Improvements to AllenNLP coreference resolver:
https://github.com/Laxminarayen/coreference-resolution-allenNLP/blob/main/improvements_to_allennlp_cr.ipynb
"""


def is_containing_other_spans(
    span: typing.List[int], all_spans: typing.List[typing.List[int]]
):
    return any([s[0] >= span[0] and s[1] <= span[1] and s != span for s in all_spans])


def get_span_noun_indices(
    doc, cluster: typing.List[typing.List[int]]
) -> typing.List[int]:
    spans = [doc[span[0] : span[1] + 1] for span in cluster]
    spans_pos = [[token.pos_ for token in span] for span in spans]
    span_noun_indices = [
        i
        for i, span_pos in enumerate(spans_pos)
        if any(pos in span_pos for pos in ["NOUN", "PROPN"])
    ]
    return span_noun_indices


def get_cluster_head(
    doc, cluster: typing.List[typing.List[int]], noun_indices: typing.List[int]
):
    head_idx = noun_indices[0]
    head_start, head_end = cluster[head_idx]
    head_span = doc[head_start : head_end + 1]
    return head_span, [head_start, head_end]


def core_logic_part(
    document, coref: typing.List[int], resolved: typing.List[str], mention_span
):
    final_token = document[coref[1]]
    if final_token.tag_ in ["PRP$", "POS"]:
        resolved[coref[0]] = mention_span.text + "'s" + final_token.whitespace_
    else:
        resolved[coref[0]] = mention_span.text + final_token.whitespace_
    for i in range(coref[0] + 1, coref[1] + 1):
        resolved[i] = ""
    return resolved


def improved_replace_corefs(document, clusters):
    resolved = list(tok.text_with_ws for tok in document)
    all_spans = [
        span for cluster in clusters for span in cluster
    ]  # flattened list of all spans
    for cluster in clusters:
        noun_indices = get_span_noun_indices(document, cluster)
        if noun_indices:
            mention_span, mention = get_cluster_head(document, cluster, noun_indices)
            for coref in cluster:
                if coref != mention and not is_containing_other_spans(coref, all_spans):
                    core_logic_part(document, coref, resolved, mention_span)
    return "".join(resolved)


class CoreferenceNormaliser(Normaliser):
    def __init__(self) -> None:
        super().__init__("coreference")
        self._predictor = Predictor.from_path(
            "https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz"
        )

    def normalise(self, text: str, context: Context) -> str:
        prediction = self._predictor.predict(document=text)
        return improved_replace_corefs(context.original_doc(), prediction["clusters"])
