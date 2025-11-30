import os
from typing import Dict

# Type alias for Roman-to-Devanagari mapping dictionaries
RomanToDevanagariMap = Dict[str, str]

# Digit mappings: ASCII digits → Devanagari digits
DIGIT_MAP: RomanToDevanagariMap = {
    "0": "०",
    "1": "१",
    "2": "२",
    "3": "३",
    "4": "४",
    "5": "५",
    "6": "६",
    "7": "७",
    "8": "८",
    "9": "९",
}

# Independent vowel forms (used when vowel appears alone or at start)
INDEPENDENT_VOWELS: RomanToDevanagariMap = {
    "a": "अ",
    "aa": "आ",
    "A": "आ",
    "i": "इ",
    "I": "इ",
    "ee": "ई",
    "ii": "ई",
    "u": "उ",
    "U": "उ",
    "oo": "ऊ",
    "uu": "ऊ",
    "Ri": "ऋ",
    "R": "ऋ",  # vocalic R
    "Ree": "ॠ",
    "lRi": "ऌ",  # vocalic L (rare)
    "e": "ए",
    "ai": "ऐ",
    "o": "ओ",
    "au": "ौ",  # Wait, au independent is औ. Fixed below.
}

# Fix au independent
INDEPENDENT_VOWELS["au"] = "औ"

# Vowel signs (matras) — attached to consonants
# Note: 'a' is inherent, so it maps to empty string effectively in combination logic
VOWEL_SIGNS: RomanToDevanagariMap = {
    "a": "",  # inherent a
    "aa": "ा",
    "A": "ा",
    "i": "ि",
    "I": "ि",
    "ee": "ी",
    "ii": "ी",
    "u": "ु",
    "U": "ु",
    "oo": "ू",
    "uu": "ू",
    "Ri": "ृ",
    "R": "ृ",
    "Ree": "ॄ",
    "e": "े",
    "ai": "ै",
    "o": "ो",
    "au": "ौ",
}

# Base consonant forms (Schwa forms, i.e., with inherent 'a')
BASE_CONSONANTS: RomanToDevanagariMap = {
    "k": "क",
    "kh": "ख",
    "g": "ग",
    "gh": "घ",
    "ng": "ङ",
    "ch": "च",
    "chh": "छ",
    "j": "ज",
    "jh": "झ",
    "ny": "ञ",
    "T": "ट",
    "Th": "ठ",
    "D": "ड",
    "Dh": "ढ",
    "N": "ण",
    "t": "त",
    "th": "थ",
    "d": "द",
    "dh": "ध",
    "n": "न",
    "p": "प",
    "ph": "फ",
    "f": "फ",
    "b": "ब",
    "bh": "भ",
    "m": "म",
    "y": "य",
    "r": "र",
    "l": "ल",
    "v": "व",
    "w": "व",
    "sh": "श",
    "Sh": "ष",
    "s": "स",
    "h": "ह",
    "ksh": "क्ष",
    "tra": "त्र",
    "gy": "ज्ञ",
    "shr": "श्र",
}

# Special overrides (for irregular forms or symbols)
SPECIAL_OVERRIDES: RomanToDevanagariMap = {
    "om": "ॐ",
    "Om": "ॐ",
    "aum": "ॐ",
    # 'gya': 'ज्ञा', # Removed as it conflicts with standard 'gy' + 'a' -> 'ज्ञ'
}

PUNCTUATION: RomanToDevanagariMap = {
    ".": "।",  # danda
    "..": "॥",  # double danda
    "|": "।",
    "||": "॥",
    "M": "ं",  # anusvara
    "m": "ं",  # common usage at word end? No, m is म. M is anusvara.
    # But often 'ram' -> 'राम'. 'm' at end is halanta 'm'.
    # We will stick to 'm' -> 'म्' (halanta) or 'म' (schwa) via standard logic.
    # If user wants anusvara, they should use 'M'.
    # However, some maps use 'm' for anusvara if it's not a vowel?
    # Let's keep 'M' for anusvara.
}


def build_roman_to_devanagari_map() -> RomanToDevanagariMap:
    """
    Builds a complete Roman-to-Devanagari transliteration mapping.
    Prioritizes longer keys first for correct greedy matching.
    """
    full_map: RomanToDevanagariMap = {}

    # 1. Independent vowels
    full_map.update(INDEPENDENT_VOWELS)

    # 2. Consonants and their combinations
    halanta = "्"

    for rom_cons, dev_cons in BASE_CONSONANTS.items():
        # Case 1: Consonant alone (halanta form)
        # e.g., 'k' -> 'क्'
        # But wait, if I type 'k', do I want 'क्' or 'क'?
        # Usually in these tools, 'k' -> 'क्' allows 'k' + 't' -> 'क्त'.
        # If I want 'क', I type 'ka'.
        # However, at the end of the word, 'k' often means 'क' (schwa deleted).
        # But for a simple mapper, 'k' -> 'क्' is safer for conjuncts.
        # User must type 'ka' for 'क'.
        full_map[rom_cons] = dev_cons + halanta

        # Case 2: Consonant + 'a' (Schwa form)
        # e.g., 'ka' -> 'क'
        full_map[rom_cons + "a"] = dev_cons

        # Case 3: Consonant + other vowels
        for rom_vowel, matra in VOWEL_SIGNS.items():
            if rom_vowel == "a":
                continue  # Handled above

            # e.g., 'kaa' -> 'क' + 'ा' = 'का'
            full_map[rom_cons + rom_vowel] = dev_cons + matra

    # 3. Punctuation and Digits
    full_map.update(PUNCTUATION)
    full_map.update(DIGIT_MAP)

    # 4. Special Overrides
    full_map.update(SPECIAL_OVERRIDES)

    # 5. Ensure 'a' maps to 'अ' (already in INDEPENDENT_VOWELS)

    # Sort by length descending
    return dict(sorted(full_map.items(), key=lambda x: len(x[0]), reverse=True))


def load_custom_word_mappings() -> RomanToDevanagariMap:
    """
    Loads custom word-level transliterations from a file.
    """
    custom_map: RomanToDevanagariMap = {}
    # Use absolute path relative to this file
    filepath = os.path.join(os.path.dirname(__file__), "word_maps.txt")

    if not os.path.exists(filepath):
        return custom_map

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    roman, devanagari = parts
                    custom_map[roman.lower()] = devanagari
    except Exception as e:
        print(f"Error reading word_maps.txt: {e}")

    return custom_map
