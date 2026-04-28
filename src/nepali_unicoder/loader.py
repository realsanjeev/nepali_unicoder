import json
import os

from nepali_unicoder.trie import Trie


def load_json_data(filename):
    path = os.path.join(os.path.dirname(__file__), "data", filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Rule file {filename} not found.")
        return {}


class RuleLoader:
    def __init__(self):
        self.word_maps_path = os.path.join(
            os.path.dirname(__file__), "data", "word_maps.json"
        )

    def load(self) -> Trie:
        """Load rules and custom mappings into a Trie."""
        trie = Trie()
        self._load_rules(trie)
        self._load_custom_mappings(trie)
        return trie

    def _load_rules(self, trie: Trie):
        data = load_json_data("roman_rules.json")

        consonants = data.get("consonants", {})
        vowels = data.get("vowels", {})
        matras = data.get("matras", {})
        special = data.get("special", {})
        digits = data.get("digits", {})

        # 1. Consonants and Combinations (inserted BEFORE vowels so that
        #    independent vowel keys inserted next will override any collision,
        #    e.g. 'lRi' consonant+matra combo is overridden by vowel 'lRi' -> ऌ)
        halanta = "्"

        for rom_cons, dev_cons in consonants.items():
            # Case 1: Consonant alone (halanta form) -> 'k' -> 'क्'
            trie.add(rom_cons, dev_cons + halanta)

            # Case 2: Consonant + 'a' (Schwa form) -> 'ka' -> 'क'
            trie.add(rom_cons + "a", dev_cons)

            # Case 3: Consonant + other vowels -> 'ki' -> 'कि'
            for rom_vowel, matra in matras.items():
                if rom_vowel == "a":
                    continue  # Handled above
                trie.add(rom_cons + rom_vowel, dev_cons + matra)

        # 1b. Compound consonants whose romanization ends in a vowel-like letter
        #     (e.g. 'tra' -> 'त्र') -- these CANNOT go through the normal consonant
        #     loop because appending 'a' for the schwa would yield 'traa' not 'tra'.
        #     Instead we build their combos explicitly:
        #       'tra'  -> 'त्र'   (natural: the trailing 'a' IS the schwa)
        #       'tra'  + matra -> 'त्र' + matra  (e.g. 'trai' -> 'त्रि')
        #       'tra'  + halanta -> 'त्र्'  (explicit halanta: append 'H' or use '{}')
        compound_consonants = data.get("compound_consonants", {})
        for rom_stem, dev_stem in compound_consonants.items():
            # Schwa form: the romanization itself (e.g. 'tra' -> 'त्र')
            trie.add(rom_stem, dev_stem)
            # With other vowels / matras (e.g. 'trai' -> 'त्रि')
            for rom_vowel, matra in matras.items():
                if rom_vowel == "a":
                    continue  # schwa already covered above
                trie.add(rom_stem + rom_vowel, dev_stem + matra)

        # 2. Independent Vowels (inserted AFTER consonant combos so they win
        #    on collision, e.g. 'lRi' -> ऌ overrides 'l'+'Ri' -> लृ)
        for rom, dev in vowels.items():
            trie.add(rom, dev)

        # 3. Special, Digits, Punctuation
        for rom, dev in special.items():
            trie.add(rom, dev)

        for rom, dev in digits.items():
            trie.add(rom, dev)

    def _load_custom_mappings(self, trie: Trie):
        if not os.path.exists(self.word_maps_path):
            return

        try:
            with open(self.word_maps_path, "r", encoding="utf-8") as f:
                mappings = json.load(f)
                for roman, devanagari in mappings.items():
                    trie.add(roman, devanagari)
                    # Automatically add capitalized version if it doesn't exist
                    # (e.g. if 'nepal' is in maps, also add 'Nepal')
                    cap_roman = roman.capitalize()
                    if cap_roman not in mappings:
                        trie.add(cap_roman, devanagari)
        except Exception as e:
            print(f"Error reading word_maps.json: {e}")


class PreetiLoader:
    def __init__(self):
        pass

    def load(self) -> Trie:
        """Load Preeti rules into a Trie."""
        trie = Trie()
        data = load_json_data("preeti_rules.json")

        mappings = data.get("mappings", {})
        for key, value in mappings.items():
            trie.add(key, value)

        return trie

    def get_post_rules(self):
        data = load_json_data("preeti_rules.json")
        return data.get("post_rules", [])
