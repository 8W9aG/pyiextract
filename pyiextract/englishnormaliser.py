from langdetect import detect

from .normaliser import Normaliser
from .context import Context


class EnglishNormaliser(Normaliser):
    def __init__(self) -> None:
        super().__init__("english")

    def normalise(self, text: str, context: Context) -> str:
        if detect(text) != "en":
            raise ValueError(f"Text not in English: {text}")
        return text
