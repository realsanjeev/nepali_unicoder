import os
import sys
import unittest

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from nepali_unicoder.convert import Converter


class TestNepaliUnicoder(unittest.TestCase):
    def setUp(self):
        self.converter = Converter()

    def test_basic_consonants(self):
        # k -> क् (halanta)
        self.assertEqual(self.converter.convert("k"), "क्")
        # ka -> क (schwa)
        self.assertEqual(self.converter.convert("ka"), "क")
        # kaa -> का (aa)
        self.assertEqual(self.converter.convert("kaa"), "का")

        # kh -> ख्
        self.assertEqual(self.converter.convert("kh"), "ख्")
        # kha -> ख
        self.assertEqual(self.converter.convert("kha"), "ख")

    def test_words(self):
        self.assertEqual(self.converter.convert("namaste"), "नमस्ते")
        # nepaala -> ne (ने) pa (प) -> paa (पा) la (ल)
        # nepaala -> नेपाल
        self.assertEqual(self.converter.convert("nepaala"), "नेपाल")
        self.assertEqual(self.converter.convert("mero"), "मेरो")
        # naam -> नाम्. naama -> नाम
        self.assertEqual(self.converter.convert("naama"), "नाम")
        # bhaat -> भात्. bhaata -> भात
        self.assertEqual(self.converter.convert("bhaata"), "भात")

    def test_vowels(self):
        self.assertEqual(self.converter.convert("a"), "अ")
        self.assertEqual(self.converter.convert("aa"), "आ")
        self.assertEqual(self.converter.convert("i"), "इ")
        self.assertEqual(self.converter.convert("u"), "उ")

        # Matras
        self.assertEqual(self.converter.convert("ki"), "कि")
        self.assertEqual(self.converter.convert("kee"), "की")
        self.assertEqual(self.converter.convert("ku"), "कु")
        self.assertEqual(self.converter.convert("koo"), "कू")
        self.assertEqual(self.converter.convert("ke"), "के")
        self.assertEqual(self.converter.convert("kai"), "कै")
        self.assertEqual(self.converter.convert("ko"), "को")
        self.assertEqual(self.converter.convert("kau"), "कौ")

    def test_special_chars(self):
        self.assertEqual(self.converter.convert("."), "।")
        self.assertEqual(self.converter.convert(".."), "॥")
        self.assertEqual(self.converter.convert("0123456789"), "०१२३४५६७८९")

    def test_as_is_block(self):
        self.assertEqual(self.converter.convert("{english}"), "english")
        self.assertEqual(self.converter.convert("mero {name} ho"), "मेरो name हो")
        self.assertEqual(self.converter.convert("{{"), "{")

    def test_conjuncts(self):
        # k + t -> क्त
        self.assertEqual(self.converter.convert("kt"), "क्त्")

        # gy -> ज्ञ (base) -> ज्ञ् (halanta)
        self.assertEqual(self.converter.convert("gy"), "ज्ञ्")
        # gya -> ज्ञ
        self.assertEqual(self.converter.convert("gya"), "ज्ञ")
        # gyaana -> ज्ञान
        self.assertEqual(self.converter.convert("gyaana"), "ज्ञान")


if __name__ == "__main__":
    unittest.main()
