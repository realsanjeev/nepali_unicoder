# Nepali Unicoder

A robust Python package for converting Romanized Nepali text into Devanagari script. It uses a greedy matching algorithm to ensure accurate transliteration and supports custom word mappings and "as-is" blocks for English text.

## Features

- **Accurate Transliteration**: Uses a greedy matching algorithm to prioritize longer phonetic matches (e.g., 'kha' is matched before 'k' and 'h').
- **Smart Vowel Handling**: Distinguishes between independent vowels (e.g., 'aa' -> 'आ') and vowel signs/matras (e.g., 'ka' -> 'क', 'kaa' -> 'का').
- **Mixed Content Support**: Allows keeping English words or specific text in Roman script using `{}` blocks.
- **Customizable**: Supports custom word-level overrides via `word_maps.json`.
- **CLI Support**: Can be used directly from the command line.

## Installation

You can install the package locally:

```bash
pip install .
```

## Usage

### Command Line Interface (CLI)

You can use the converter directly from the terminal:

```bash
# Direct argument
python -m nepali_unicoder.convert "namaste"
# Output: नमस्ते

# Pipe input
echo "mero naam sanjeev ho" | python -m nepali_unicoder.convert
# Output: मेरो नाम सन्जीव् हो
```

### Python API

```python
from nepali_unicoder import Converter

converter = Converter()

# Basic conversion
text = "namaste nepal"
print(converter.convert(text))
# Output: नमस्ते नेपाल

# Using 'as-is' blocks for English text
mixed_text = "mero naam {Sanjeev} ho"
print(converter.convert(mixed_text))
# Output: मेरो नाम Sanjeev हो
```

## Transliteration Rules

- **Consonants**: `k` -> `क्`, `ka` -> `क`, `kh` -> `ख्`, `kha` -> `ख`
- **Vowels**: `a` -> `अ`, `aa` -> `आ`, `i` -> `इ`, `u` -> `उ`
- **Matras**: `ki` -> `कि`, `ko` -> `को`
- **Special**: `.` -> `।`, `..` -> `॥`

## Development

To run tests:

```bash
python -m unittest discover tests
```

## License

MIT
