import re
import sys
import typing

from Levenshtein import distance


def best_fit_index(text: str, substring: str) -> int:
    if len(substring) > len(text):
        return 0
    return sorted(
        [
            {"index": i, "dist": distance(substring, text[i : len(substring)])}
            for i in range(0, len(text) - len(substring))
        ],
        key=lambda x: x["dist"],
    )[0]["index"]


def find_indexes(text: str, substring: str) -> typing.List[int]:
    indexes = [x.start() for x in re.finditer(text, substring)]
    if not indexes:
        indexes = [best_fit_index(text, substring)]
    return indexes


def find_closest_index(text: str, entity: str, relation: str) -> int:
    relation_indexes = find_indexes(text, relation)
    entity_indexes = find_indexes(text, entity)
    min_distance = sys.maxsize
    min_entity_index = 0
    for entity_index in entity_indexes:
        for relation_index in relation_indexes:
            dist = abs(relation_index - entity_index)
            if dist < min_distance:
                min_distance = dist
                min_entity_index = entity_index
    return min_entity_index


def token_ids_span(
    span: typing.Any, entity_idx: int, entity_text: str
) -> typing.Tuple[int, int]:
    idx_start = 0
    idx_end = 0
    for token in span:
        if token.idx == entity_idx:
            idx_start = token.i
        elif token.idx < entity_idx + len(entity_text):
            idx_end = token.i
    return idx_start, idx_end


def extract_entities_span(
    span: typing.Any, head_entity_text: str, relation_text: str, tail_entity_text: str
) -> typing.Tuple[typing.Any, typing.Any]:
    head_entity_idx = find_closest_index(str(span), head_entity_text, relation_text)
    tail_entity_idx = find_closest_index(str(span), tail_entity_text, relation_text)
    head_entity_idx_start, head_entity_idx_end = token_ids_span(
        span, head_entity_idx, head_entity_text
    )
    tail_entity_idx_start, tail_entity_idx_end = token_ids_span(
        span, tail_entity_idx, tail_entity_text
    )
    head_entity = span[head_entity_idx_start:head_entity_idx_end]
    tail_entity = span[tail_entity_idx_start:tail_entity_idx_end]
    return head_entity, tail_entity
