# API Reference

This document provides technical details about the classes and methods available in the **Nepali Unicoder** package.

## `Converter` Class

The `Converter` class is a simplified wrapper around the `Engine` for easy usage.

### `__init__(self, mode: str = "roman")`
Initializes a new `Converter`.
- **`mode`**: Either `"roman"` (default) or `"preeti"`.

### `convert(self, text: str) -> str`
Translates the input text to Unicode Devanagari.
- **`text`**: The input string (Romanized Nepali or Preeti characters).

---

## `Engine` Class

The core conversion logic is implemented in the `Engine` class.

### `__init__(self, trie: Optional[Trie] = None, tokenizer: Optional[Tokenizer] = None, mode: str = "roman")`
Initializes the conversion engine.
- Loads the appropriate character mappings into a `Trie` based on the `mode`.
- Loads `post_rules` for contextual transformations in Preeti mode.

---

## `Tokenizer` Class

The `Tokenizer` splits the input text into meaningful chunks (Tokens).

### `tokenize(self, text: str, use_blocks: bool = True) -> List[Token]`
Splits text into tokens based on types: `ROMAN`, `BLOCK`, `LITERAL`, and `NUMBER`.
- **`use_blocks`**: If `True` (default), recognizes `{...}` as "as-is" blocks. In Preeti mode, this is typically set to `False` by the `Engine`.
