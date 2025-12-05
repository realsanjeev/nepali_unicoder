import json
import os
from dataclasses import dataclass
from typing import List

from nepali_unicoder.fst import FST


@dataclass
class Token:
    value: str
    type: str  # 'ROMAN', 'BLOCK', 'PUNCTUATION', 'UNKNOWN'


class Engine:
    def __init__(self):
        self.fst = FST()
        self.load_rules()
        self.load_custom_mappings()

    def load_rules(self):
        """Load rules from JSON and populate the FST."""
        rules_path = os.path.join(os.path.dirname(__file__), "rules.json")
        if not os.path.exists(rules_path):
            raise FileNotFoundError(f"Rules file not found: {rules_path}")

        with open(rules_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        consonants = data.get("consonants", {})
        vowels = data.get("vowels", {})
        matras = data.get("matras", {})
        special = data.get("special", {})
        digits = data.get("digits", {})

        # 1. Independent Vowels
        for rom, dev in vowels.items():
            self.fst.add_mapping(rom, dev)

        # 2. Consonants and Combinations
        halanta = "्"

        for rom_cons, dev_cons in consonants.items():
            # Case 1: Consonant alone (halanta form) -> 'k' -> 'क्'
            self.fst.add_mapping(rom_cons, dev_cons + halanta)

            # Case 2: Consonant + 'a' (Schwa form) -> 'ka' -> 'क'
            self.fst.add_mapping(rom_cons + "a", dev_cons)

            # Case 3: Consonant + other vowels -> 'ki' -> 'कि'
            for rom_vowel, matra in matras.items():
                if rom_vowel == "a":
                    continue  # Handled above
                self.fst.add_mapping(rom_cons + rom_vowel, dev_cons + matra)

        # 3. Special, Digits, Punctuation
        for rom, dev in special.items():
            self.fst.add_mapping(rom, dev)

        for rom, dev in digits.items():
            self.fst.add_mapping(rom, dev)

        # Ensure 'a' maps to 'अ' (already in vowels, but good to double check)
        self.fst.add_mapping("a", vowels.get("a", "अ"))

    def load_custom_mappings(self):
        """Load custom word mappings from word_maps.json."""
        filepath = os.path.join(os.path.dirname(__file__), "word_maps.json")
        if not os.path.exists(filepath):
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                mappings = json.load(f)
                for roman, devanagari in mappings.items():
                    self.fst.add_mapping(roman.lower(), devanagari)
        except Exception as e:
            print(f"Error reading word_maps.json: {e}")

    def tokenize(self, text: str) -> List[Token]:
        """
        Split text into tokens.
        This simple tokenizer handles {blocks} and treats everything else as ROMAN for now.
        """
        tokens = []
        i = 0
        n = len(text)

        while i < n:
            if text[i] == "{":
                # Check for escape {{
                if i + 1 < n and text[i + 1] == "{":
                    # Actually, if it's escaped, it should probably be treated as a literal '{' in the output.
                    tokens.append(Token(value="{", type="LITERAL"))
                    i += 2
                else:
                    # Start of block
                    j = i + 1
                    while j < n and text[j] != "}":
                        j += 1

                    if j < n:  # Found closing brace
                        content = text[i + 1 : j]
                        tokens.append(Token(value=content, type="BLOCK"))
                        i = j + 1
                    else:  # Unclosed brace, treat as literal
                        tokens.append(Token(value="{", type="LITERAL"))
                        i += 1
            elif text[i] == "}":
                # Unmatched closing brace, treat as literal
                tokens.append(Token(value="}", type="LITERAL"))
                i += 1
            else:
                # Accumulate Roman text
                j = i
                while j < n and text[j] not in "{}":
                    j += 1
                tokens.append(Token(value=text[i:j], type="ROMAN"))
                i = j

        return tokens

    def transliterate(self, text: str) -> str:
        """
        Convert Roman text to Devanagari using the FST.
        """
        if not text:
            return ""

        tokens = self.tokenize(text)
        result = []

        for token in tokens:
            if token.type == "BLOCK":
                result.append(token.value)
            elif token.type == "LITERAL":
                result.append(token.value)
            elif token.type == "ROMAN":
                # Process Roman chunk with FST
                chunk = token.value
                idx = 0
                chunk_len = len(chunk)

                while idx < chunk_len:
                    # Try to find longest match starting at idx
                    sub = chunk[idx:]
                    match_val, match_len = self.fst.longest_match(sub)

                    if match_val:
                        result.append(match_val)
                        idx += match_len
                    else:
                        # No match, keep character as is
                        result.append(chunk[idx])
                        idx += 1

        return "".join(result)
