# Usage Guide

This guide describes how to use **Nepali Unicoder** through its Command Line Interface (CLI) and Python API.

## Installation

```bash
pip install nepali-unicoder
```

## Python API

The primary interface is the `Converter` class.

### Roman to Unicode Mode (Default)

```python
from nepali_unicoder.convert import Converter

# Initialize converter
converter = Converter()

# Convert phonetic Roman text
print(converter.convert("namaste")) 
# Output: नमस्ते
```

### Preeti to Unicode Mode

```python
# Initialize converter in Preeti mode
preeti_converter = Converter(mode="preeti")

# Convert Preeti characters
print(preeti_converter.convert("s{sf"))
# Output: र्कर्का
```

### Handling Mixed English Content

You can wrap English words or any text you want to preserve in curly braces `{}`.

```python
text = "mero {name} sanjeev ho."
print(converter.convert(text))
# Output: मेरो name सन्जीव् हो।
```

!!! note "English Preservation"
    In **Preeti mode**, the curly braces `{` and `}` are treated as normal characters because they are part of the Preeti font mapping.

## Command Line Interface

You can run the package directly from your shell.

### Basic Usage

```bash
python -m nepali_unicoder "nepaala"
# Output: नेपाल
```

### Preeti Conversion

Use the `--preeti` flag for Preeti font text.

```bash
python -m nepali_unicoder --preeti "s{sf"
# Output: र्कर्का
```

### Piping Input

```bash
echo "mero naam sanjeev ho" | python -m nepali_unicoder
# Output: मेरो नाम सन्जीव् हो
```
