from __future__ import annotations

from nepali_unicoder.engine import Engine


class Converter:
    """
    Wrapper around Engine for backward compatibility.
    """

    def __init__(self, mode: str = "roman", word_map: dict[str, str] | None = None):
        self.engine = Engine(mode=mode, word_map=word_map)

    def convert(self, text: str) -> str:
        return self.engine.transliterate(text)
