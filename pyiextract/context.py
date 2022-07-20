import typing

from .spacy import NLP


class Context:
    def __init__(self, original_text: str) -> None:
        self._original_text = original_text
        self._original_doc: typing.Any = None
        self._resolved_doc: typing.Any = None
        self._resolved_text = original_text

    def original_text(self) -> str:
        return self._original_text

    def original_doc(self) -> typing.Any:
        if self._original_doc is None:
            self._original_doc = NLP(self._original_text)
        return self._original_doc

    def set_resolved_text(self, resolved_text: str) -> None:
        self._resolved_text = resolved_text
        self._resolved_doc = None

    def resolved_text(self) -> str:
        return self._resolved_text

    def resolved_doc(self) -> typing.Any:
        if self._resolved_text is None:
            return None
        if self._resolved_doc is None:
            self._resolved_doc = NLP(self._resolved_text)
        return self._resolved_doc
