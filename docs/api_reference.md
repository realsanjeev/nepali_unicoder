# API Reference

This document provides technical details about the classes and methods available in the **Nepali Unicoder** package.

## `Converter` Class

The `Converter` class is a simplified wrapper around the `Engine` for easy usage.

### `__init__(self, mode: str = "roman", word_map: Optional[Dict[str, str]] = None)`
Initializes a new `Converter`.
- **`mode`**: Either `"roman"` (default) or `"preeti"`.
- **`word_map`**: Extra whole-word mappings (Roman mode only). They override bundled
  entries and get a capitalized variant automatically. Keys must be ASCII letters only;
  otherwise `ValueError` is raised.

### `convert(self, text: str) -> str`
Translates the input text to Unicode Devanagari.
- **`text`**: The input string (Romanized Nepali or Preeti characters).

---

## `Engine` Class

The core conversion logic is implemented in the `Engine` class.

### `__init__(self, trie: Optional[Trie] = None, tokenizer: Optional[Tokenizer] = None, mode: str = "roman", word_map: Optional[Dict[str, str]] = None)`
Initializes the conversion engine.
- Loads the appropriate character mappings into a `Trie` based on the `mode`. Each mode's
  tables are built once per process and shared by all engines, so treat `engine.trie` as read-only.
- **`word_map`**: see `Converter`.
- Loads `post_rules` for contextual transformations in Preeti mode.

---

## `Tokenizer` Class

The `Tokenizer` splits the input text into meaningful chunks (Tokens).

### `tokenize(self, text: str) -> list[Token]`
Splits text into tokens based on types: `ROMAN`, `BLOCK`, `LITERAL`, and `NUMBER`.
`{...}` is kept as an "as-is" block. Used in Roman mode only; Preeti text is mapped as a whole.
