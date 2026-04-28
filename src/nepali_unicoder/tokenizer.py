import re
from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    value: str
    type: str  # 'ROMAN', 'BLOCK', 'PUNCTUATION', 'UNKNOWN', 'LITERAL', 'NUMBER'


class Tokenizer:
    # Compiled once at class definition time -- not per tokenize() call.
    _RE_BLOCK = re.compile(r"\{([^}]*)\}")
    _RE_NUMBER = re.compile(r"\d*\.\d+|\d+")

    def tokenize(self, text: str, use_blocks: bool = True) -> List[Token]:
        """
        Split text into tokens using regex-based matching for robustness.
        """
        tokens = []
        i = 0
        n = len(text)
        roman_buffer = []

        re_block = self._RE_BLOCK
        re_number = self._RE_NUMBER

        def flush_roman():
            if roman_buffer:
                tokens.append(Token(value="".join(roman_buffer), type="ROMAN"))
                roman_buffer.clear()

        while i < n:
            # 1. Check for Ellipsis (Priority)
            if text.startswith("...", i):
                flush_roman()
                tokens.append(Token(value="...", type="LITERAL"))
                i += 3
                continue

            # 2. Check for Blocks and Braces (if enabled)
            if use_blocks:
                # Escaped brace {{
                if text.startswith("{{", i):
                    flush_roman()
                    tokens.append(Token(value="{", type="LITERAL"))
                    i += 2
                    continue

                # Block {content}
                match_block = re_block.match(text, i)
                if match_block:
                    flush_roman()
                    tokens.append(Token(value=match_block.group(1), type="BLOCK"))
                    i = match_block.end()
                    continue

                # Escaped brace }}
                if text.startswith("}}", i):
                    flush_roman()
                    tokens.append(Token(value="}", type="LITERAL"))
                    i += 2
                    continue

                # Unmatched closing brace }
                if text.startswith("}", i):
                    flush_roman()
                    tokens.append(Token(value="}", type="LITERAL"))
                    i += 1
                    continue

                # Unmatched opening brace {
                if text.startswith("{", i):
                    flush_roman()
                    tokens.append(Token(value="{", type="LITERAL"))
                    i += 1
                    continue

            # 3. Check for Numbers
            match_number = re_number.match(text, i)
            if match_number:
                flush_roman()
                tokens.append(Token(value=match_number.group(0), type="NUMBER"))
                i = match_number.end()
                continue

            # 4. Fallback: Accumulate Roman
            roman_buffer.append(text[i])
            i += 1

        flush_roman()
        return tokens
