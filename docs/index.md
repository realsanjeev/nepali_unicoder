# Nepali Unicoder Documentation

Welcome to the official documentation for **Nepali Unicoder**, a robust Python package for converting Romanized Nepali text and Preeti font text into Unicode Devanagari script.

## Overview

Nepali Unicoder provides tools to handle the complexities of Devanagari script conversion, including contextual rules for Preeti font and a greedy matching algorithm for Roman transliteration.

## Documentation Sections

- [**Getting Started**](./usage.md): Learn how to install and use the package via CLI and Python API.
- [**Preeti Mapping Reference**](./preeti_mappings.md): A comprehensive guide to Preeti character mappings and contextual rules.
- [**API Reference**](./api_reference.md): Technical details about the project's classes and methods.

## Key Features

- **Greedy Phonetic Matching**: Prioritizes longer matches for more accurate Roman-to-Unicode conversion.
- **Extensive Preeti Support**: Over 40+ mappings and contextual rules (reph, matras, combined forms).
- **English Block Support**: Use `{}` to preserve English text within converted strings.
- **Custom Overrides**: Add custom word-level mappings via `word_maps.json`.
