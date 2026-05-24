import os
import sys
import unittest

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from nepali_unicoder import Converter  # public API export (Fix #10)
from nepali_unicoder.loader import RuleLoader
from nepali_unicoder.tokenizer import Tokenizer
from nepali_unicoder.trie import Trie


class TestTrie(unittest.TestCase):
    def test_add_and_match(self):
        trie = Trie()
        trie.add("ka", "क")
        trie.add("k", "क्")

        val, length = trie.longest_match("ka")
        self.assertEqual(val, "क")
        self.assertEqual(length, 2)

        val, length = trie.longest_match("k")
        self.assertEqual(val, "क्")
        self.assertEqual(length, 1)

        val, length = trie.longest_match("z")
        self.assertIsNone(val)
        self.assertEqual(length, 0)


class TestTokenizer(unittest.TestCase):
    def test_tokenize(self):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("mero {name} ho")

        self.assertEqual(len(tokens), 3)
        self.assertEqual(tokens[0].value, "mero ")
        self.assertEqual(tokens[0].type, "ROMAN")

        self.assertEqual(tokens[1].value, "name")
        self.assertEqual(tokens[1].type, "BLOCK")

        self.assertEqual(tokens[2].value, " ho")
        self.assertEqual(tokens[2].type, "ROMAN")

    def test_escape(self):
        """{{ should produce literal {."""
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("{{")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].value, "{")
        self.assertEqual(tokens[0].type, "LITERAL")

    def test_closing_brace_escape(self):
        """Fix #6: }} should produce literal } symmetrically with {{."""
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("}}")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].value, "}")
        self.assertEqual(tokens[0].type, "LITERAL")

    def test_number_leading_dot(self):
        """Fix #7: a leading-dot decimal like .5 must be tokenized as NUMBER
        not as ROMAN '.' followed by a separate NUMBER."""
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(".5")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].value, ".5")
        self.assertEqual(tokens[0].type, "NUMBER")

    def test_number_integer_and_decimal(self):
        """Standard integer and decimal numbers still tokenize correctly."""
        tokenizer = Tokenizer()

        tokens = tokenizer.tokenize("123")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, "NUMBER")

        tokens = tokenizer.tokenize("10.5")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, "NUMBER")
        self.assertEqual(tokens[0].value, "10.5")


class TestRuleLoader(unittest.TestCase):
    def setUp(self):
        self.loader = RuleLoader()
        self.trie = self.loader.load()

    def test_load(self):
        self.assertIsInstance(self.trie, Trie)
        val, length = self.trie.longest_match("ka")
        self.assertEqual(val, "क")
        self.assertEqual(length, 2)

    def test_lRi_vowel_not_overwritten(self):
        """Fix #1: after inserting consonant+matra combos first and vowels last,
        the trie must return the independent vowel ऌ for 'lRi', NOT लृ."""
        val, length = self.trie.longest_match("lRi")
        self.assertEqual(val, "ऌ")
        self.assertEqual(length, 3)

    def test_compound_consonant_tra(self):
        """Fix #2: 'tra' must map to त्र (schwa form), not त्र् (halanta)."""
        val, length = self.trie.longest_match("tra")
        self.assertEqual(val, "त्र")
        self.assertEqual(length, 3)

        val, _ = self.trie.longest_match("tri")
        self.assertEqual(val, "त्रि")

        val, _ = self.trie.longest_match("trai")
        self.assertEqual(val, "त्रै")

        val, _ = self.trie.longest_match("traa")
        self.assertEqual(val, "त्रा")


class TestPublicAPI(unittest.TestCase):
    """Fix #10: Converter must be importable directly from the package root."""

    def test_import_from_package_root(self):
        # Import at module level already asserts this; just confirm it's the
        # same class as the one in convert.py
        from nepali_unicoder.convert import Converter as _Converter
        self.assertIs(Converter, _Converter)

    def test_basic_conversion_via_public_api(self):
        c = Converter()
        self.assertEqual(c.convert("namaste"), "नमस्ते")

    def test_preeti_mode_via_public_api(self):
        c = Converter(mode="preeti")
        self.assertEqual(c.convert("s{"), "र्क")



if __name__ == "__main__":
    unittest.main()
