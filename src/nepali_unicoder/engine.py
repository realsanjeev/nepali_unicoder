from __future__ import annotations

import re
from functools import lru_cache

from nepali_unicoder.loader import (
    PreetiLoader,
    RuleLoader,
    load_json_data,
    with_capitalized,
)
from nepali_unicoder.tokenizer import Token, Tokenizer
from nepali_unicoder.trie import Trie

_RE_WORD = re.compile(r"[A-Za-z]+")


@lru_cache(maxsize=None)
def _load_defaults(mode: str):
    """Build a mode's (trie, post_rules, word_map) once per process.
    Shared by every Engine, so treat them as read-only."""
    if mode == "preeti":
        loader = PreetiLoader()
        post_rules = tuple(
            (re.compile(pattern, re.MULTILINE), replacement)
            for pattern, replacement in loader.get_post_rules()
        )
        return loader.load(), post_rules, {}
    word_map = with_capitalized(load_json_data("word_maps.json"))
    return RuleLoader().load(), (), word_map


class Engine:
    VALID_MODES = frozenset({"roman", "preeti"})

    def __init__(
        self,
        trie: Trie | None = None,
        tokenizer: Tokenizer | None = None,
        mode: str = "roman",
        word_map: dict[str, str] | None = None,
    ):
        if mode not in self.VALID_MODES:
            raise ValueError(
                f"Invalid mode {mode!r}. Expected one of {sorted(self.VALID_MODES)}"
            )
        if word_map:
            if mode != "roman":
                raise ValueError("word_map is only supported in 'roman' mode")
            bad = [key for key in word_map if not _RE_WORD.fullmatch(key)]
            if bad:
                raise ValueError(
                    f"word_map keys must be single words of ASCII letters: {bad!r}"
                )
        self.mode = mode

        if trie is None:
            self.trie, post_rules, default_map = _load_defaults(mode)
        else:
            self.trie, post_rules, default_map = trie, (), {}
        self.post_rules = post_rules
        # User entries win over the bundled ones; copy so the cache stays untouched.
        self.word_map = {**default_map, **with_capitalized(word_map or {})}

        self.tokenizer = tokenizer or Tokenizer()

    def transliterate(self, text: str) -> str:
        """
        Convert Roman text to Devanagari using the Trie.
        """
        if not text:
            return ""

        if self.mode == "preeti":
            # Every Preeti key (digits, '.', braces) is a glyph: map the whole text.
            tokens = [Token(value=text, type="ROMAN")]
        else:
            tokens = self.tokenizer.tokenize(text)
        result = []

        for token in tokens:
            if token.type == "BLOCK" or token.type == "LITERAL":
                result.append(token.value)
            elif token.type == "NUMBER":
                # Process Number chunk: transliterate digits, keep others (like .) as is
                for char in token.value:
                    if char.isdigit():
                        # Use Trie to find digit mapping (digits are single chars in rules)
                        match_val, _ = self.trie.longest_match(char)
                        if match_val:
                            result.append(match_val)
                        else:
                            result.append(char)
                    else:
                        result.append(char)
            elif token.type == "ROMAN":
                # Process Roman chunk with Trie
                chunk = token.value
                idx = 0
                chunk_len = len(chunk)

                while idx < chunk_len:
                    # Word maps apply to whole words only ('bus' but not 'bushan')
                    if self.word_map and (idx == 0 or not chunk[idx - 1].isalpha()):
                        word = _RE_WORD.match(chunk, idx)
                        if word and word.group() in self.word_map:
                            result.append(self.word_map[word.group()])
                            idx = word.end()
                            continue

                    # Try to find longest match starting at idx
                    # Pass chunk and idx directly to avoid slicing
                    match_val, match_len = self.trie.longest_match(chunk, idx)

                    if match_val:
                        result.append(match_val)
                        idx += match_len
                    else:
                        # No match, keep character as is
                        result.append(chunk[idx])
                        idx += 1

        output = "".join(result)

        # Apply post-processing rules for Preeti mode
        if self.mode == "preeti" and self.post_rules:
            output = self._apply_post_rules(output)

        return output

    def _apply_post_rules(self, text: str) -> str:
        """
        Apply post-processing rules (regex replacements) to the text.
        Used for Preeti mode to handle contextual transformations.
        """
        for pattern, replacement in self.post_rules:
            text = pattern.sub(replacement, text)
        return text
