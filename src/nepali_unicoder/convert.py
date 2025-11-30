import os
import sys
from dataclasses import dataclass
from typing import Dict

# If running as script, add src to path so absolute imports work
if __name__ == "__main__":
    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
    )

from nepali_unicoder.mappings import (
    build_roman_to_devanagari_map,
    load_custom_word_mappings,
)

RomanToDevanagariMap = Dict[str, str]


@dataclass
class State:
    remaining: str
    processed: str = ""
    as_is: bool = False


class Converter:
    def __init__(self):
        # Build main mapping (longest first)
        self.main_map: RomanToDevanagariMap = build_roman_to_devanagari_map()
        self.word_maps: RomanToDevanagariMap = load_custom_word_mappings()

        # Final combined map: word overrides take highest priority
        self.full_map = self.main_map.copy()
        self.full_map.update(self.word_maps)

        # Sort by length descending — CRITICAL for correct greedy matching
        self.sorted_keys = sorted(self.full_map.keys(), key=len, reverse=True)

    def convert(self, text: str) -> str:
        """
        Convert Roman text to Devanagari using greedy matching.
        Supports:
        - Standard transliteration (e.g., 'namaste' -> 'नमस्ते')
        - As-is blocks: {text} keeps 'text' in Roman.
        - Escape: {{ -> {
        """
        if not text:
            return ""

        # We process the text from start to end
        state = State(remaining=text)

        while state.remaining:
            matched = False

            # === 1. As-is block handling: { ... } ===
            if state.as_is:
                if state.remaining.startswith("}"):
                    # End of as-is block
                    state.remaining = state.remaining[1:]
                    state.as_is = False
                    matched = True
                else:
                    # Copy character literally
                    state.processed += state.remaining[0]
                    state.remaining = state.remaining[1:]
                    matched = True

            # === 2. Start or escape curly brace ===
            elif state.remaining.startswith("{{"):
                # Escaped brace
                state.processed += "{"
                state.remaining = state.remaining[2:]
                matched = True
            elif state.remaining.startswith("{"):
                # Start of as-is block
                state.remaining = state.remaining[1:]
                state.as_is = True
                matched = True

            if matched:
                continue

            # === 3. Try full-word mappings first (highest priority) ===
            # We check if the remaining text starts with any key in our map
            # Keys are sorted by length, so we match the longest possible prefix first

            # Optimization: check only keys that match the first char?
            # For now, iterating sorted_keys is fine for small maps, but for large maps it's slow.
            # Given the map size (~100-200 keys), it's acceptable.

            lower_remaining = state.remaining.lower()

            for key in self.sorted_keys:
                # Check if remaining starts with key (case-insensitive match for key lookup)
                if lower_remaining.startswith(key):
                    # Found a match!
                    devanagari = self.full_map[key]

                    # Advance state
                    state.processed += devanagari
                    state.remaining = state.remaining[len(key) :]
                    matched = True
                    break

            # === 4. Fallback: take one character as-is (for unsupported/English text) ===
            if not matched:
                state.processed += state.remaining[0]
                state.remaining = state.remaining[1:]

        return state.processed


def main():
    if len(sys.argv) < 2:
        # Check if there is stdin
        if not sys.stdin.isatty():
            input_text = sys.stdin.read()
        else:
            print('Usage: python -m nepali_unicoder.convert "your roman text here"')
            print('       or: echo "namaste" | python -m nepali_unicoder.convert')
            return
    else:
        input_text = " ".join(sys.argv[1:])

    converter = Converter()
    result = converter.convert(input_text)
    print(result)


if __name__ == "__main__":
    main()
