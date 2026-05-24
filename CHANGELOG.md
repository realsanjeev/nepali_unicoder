# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] – 2026-04-28

### Fixed

- **`tra` compound consonant** (`roman_rules.json`): moved `tr` into the
  `consonants` section so the standard loop generates the correct schwa form
  `tra → त्र` (not the halanta form `त्र्`). All derived matras (`tri`, `traa`,
  `trai`, …) are also correct.
- **`lRi` independent vowel** (`loader.py`): consonant + matra combinations are
  now inserted into the trie *before* independent vowels, so `lRi → ऌ` wins
  over the `l + Ri-matra` combination.
- **`}}` closing-brace escape** (`tokenizer.py`): `}}` now produces a literal
  `}` token, symmetric with the existing `{{` escape.
- **Leading-dot decimal tokenization** (`tokenizer.py`): `.5` is now tokenized
  as a single `NUMBER` token instead of a ROMAN `.` followed by a `NUMBER`
  `5`, so the `.` is no longer converted to the Devanagari danda `।`.
- **README output example** (`README.md`): corrected the expected output for
  `"mero naam {Sanjeev} ho"` from `नाम` to `नाम्` — `naam` without a trailing
  vowel correctly produces the halanta form.

### Changed

- **`Converter` public API** (`__init__.py`): `Converter` is now importable
  directly from the package root (`from nepali_unicoder import Converter`).
- **Mode validation** (`engine.py`): `Engine` (and therefore `Converter`) now
  raises a clear `ValueError` immediately for an unrecognised `mode` argument
  (e.g. `Converter(mode="Preeti")`), instead of silently falling back to roman
  mode.

### Improved (code quality)

- **`import re` moved to module level** (`tokenizer.py`): the lazy `import re`
  inside `Tokenizer.tokenize()` has been moved to the top of the module,
  following PEP 8 and making the dependency visible.
- **Regex patterns compiled once** (`tokenizer.py`): `_RE_BLOCK` and
  `_RE_NUMBER` are now class-level constants on `Tokenizer`, compiled once at
  class definition time instead of on every `tokenize()` call.
- **`PreetiLoader` reads JSON once** (`loader.py`): the `preeti_rules.json`
  file is now parsed once in `PreetiLoader.__init__` and cached in
  `self._data`. Previously `load()` and `get_post_rules()` each called
  `load_json_data()` independently, causing the file to be read twice per
  `Converter(mode="preeti")` construction.
- **`except Exception` replaced with specific exceptions** (`loader.py`):
  `_load_custom_mappings` no longer silently swallows all errors. The
  bare `except Exception: print(...)` has been removed; `json.JSONDecodeError`,
  `UnicodeDecodeError`, and `OSError` now propagate naturally so callers can
  detect corrupt or unreadable `word_maps.json` files.
- **`print` replaced with `logging`** (`loader.py`): the `"Warning: Rule file
  not found"` message in `load_json_data` now uses `logging.getLogger(__name__)`
  (`nepali_unicoder.loader`) instead of `print()`, giving library users full
  control over verbosity via the standard `logging` framework.
- **PEP 8 import order** (`loader.py`): the local import
  `from nepali_unicoder.trie import Trie` is now grouped with all other imports,
  above the module-level `_logger` assignment.
- **No-op `try/except` removed** (`loader.py`): after the exception-handling
  fix, the `try/except` block in `_load_custom_mappings` only re-raised every
  branch. The block has been removed; the file is opened directly and exceptions
  propagate naturally. The `os.path.exists()` guard above it already handles
  the missing-file case.

---

## [0.1.2] – 2025-05-01

- Initial public release on PyPI.
- Roman-to-Devanagari transliteration using a greedy trie-based matching
  algorithm.
- Preeti font-to-Unicode conversion with 30+ contextual post-processing rules.
- CLI support via `python -m nepali_unicoder` and the `nepali-unicoder` entry
  point.
- `word_maps.json` for custom word-level overrides.
- GitHub Actions CI across Python 3.8–3.12.
- MkDocs documentation published to GitHub Pages.

[0.2.1]: https://github.com/realsanjeev/nepali_unicoder/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/realsanjeev/nepali_unicoder/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/realsanjeev/nepali_unicoder/releases/tag/v0.1.2
