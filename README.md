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
python -m nepali_unicoder "namaste"
# Output: नमस्ते

# Pipe input
echo "mero naam sanjeev ho" | python -m nepali_unicoder
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
- **Numbers**: `0-9` -> `०-९` (Decimal points are preserved: `1.5` -> `१.५`)

## Advanced Usage

### Handling Complex Text

The converter handles mixed content gracefully. You can use `{}` to keep text as-is (e.g., for English words or code snippets).

```python
text = "mero naam {Sanjeev} ho ra ma 12.5 barsa ko bhaye."
print(converter.convert(text))
# Output: मेरो नाम Sanjeev हो र म १२.५ बर्स को भए।
```

### Configuration

The package uses two JSON files for configuration, located in the `src/nepali_unicoder` directory:

1.  **`rules.json`**: Defines the core transliteration rules (consonants, vowels, matras, etc.).
2.  **`word_maps.json`**: Defines custom word-level overrides. Use this for words that don't follow standard phonetic rules.

Example `word_maps.json`:
```json
{
    "nepal": "नेपाल",
    "kathamandu": "काठमाडौँ"
}
```

## Contribution

We welcome contributions! Here's how you can help:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/realsanjeev/nepali_unicoder.git
    cd nepali_unicoder
    ```

2.  **Set up a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
    ```

3.  **Run tests**:
    ```bash
    python -m unittest discover tests
    ```

4.  **Submit a Pull Request**: Create a new branch, make your changes, and submit a PR.

## Development

To run tests:

```bash
python -m unittest discover tests
```

## License

MIT
