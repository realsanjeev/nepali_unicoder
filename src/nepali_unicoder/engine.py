from typing import Optional

from nepali_unicoder.loader import RuleLoader
from nepali_unicoder.tokenizer import Tokenizer
from nepali_unicoder.trie import Trie


class Engine:
    def __init__(
        self, trie: Optional[Trie] = None, tokenizer: Optional[Tokenizer] = None
    ):
        if trie is None:
            loader = RuleLoader()
            self.trie = loader.load()
        else:
            self.trie = trie

        if tokenizer is None:
            self.tokenizer = Tokenizer()
        else:
            self.tokenizer = tokenizer

    def transliterate(self, text: str) -> str:
        """
        Convert Roman text to Devanagari using the Trie.
        """
        if not text:
            return ""

        tokens = self.tokenizer.tokenize(text)
        result = []

        for token in tokens:
            if token.type == "BLOCK":
                result.append(token.value)
            elif token.type == "LITERAL":
                result.append(token.value)
            elif token.type == "ROMAN":
                # Process Roman chunk with Trie
                chunk = token.value
                idx = 0
                chunk_len = len(chunk)

                while idx < chunk_len:
                    # Try to find longest match starting at idx
                    sub = chunk[idx:]
                    match_val, match_len = self.trie.longest_match(sub)

                    if match_val:
                        result.append(match_val)
                        idx += match_len
                    else:
                        # No match, keep character as is
                        result.append(chunk[idx])
                        idx += 1

        return "".join(result)
