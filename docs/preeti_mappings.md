# Preeti Mapping Reference

This document provides a comprehensive list of Preeti character mappings and the contextual rules applied by **Nepali Unicoder**.

## Basic Mappings (a-z)

| Key | Unicode | Description |
|-----|---------|-------------|
| `a` | `ब` | |
| `b` | `द` | |
| `c` | `अ` | |
| `d` | `म` | |
| `e` | `भ` | |
| `f` | `ा` | Aa-kar |
| `g` | `न` | |
| `h` | `ज` | |
| `i` | `ष्` | |
| `j` | `व` | |
| `k` | `प` | |
| `l` | `ि` | Ee-kar (short) |
| `n` | `ल` | |
| `o` | `य` | |
| `p` | `उ` | |
| `q` | `त्र` | |
| `r` | `च` | |
| `s` | `क` | |
| `t` | `त` | |
| `u` | `ग` | |
| `v` | `ख` | |
| `w` | `ध` | |
| `x` | `ह` | |
| `y` | `थ` | |
| `z` | `श` | |

## Special Combined and Half Forms

| Character | Unicode | Description |
|-----------|---------|-------------|
| `«` / `»` | `्र` | Ra-foot (for ट, ठ, ड, ढ) |
| `¿` | `रू` | Combined ruu |
| `å` | `द्व` | Combined dva |
| `ˆ` | `फ्` | Half ph |
| `ª` | `ङ` | Consonant nga |
| `¥` | `र्` | Half ra (Reph variation) |
| `¶` | `ठ्ठ` | Combined thth |
| `§` | `ट्ट` | Combined tt |
| `£` | `घ्` | Half gh |
| `Ë` | `ङ्ग` | Combined nga-ga |
| `Í` | `ङ्क` | Combined nga-ka |
| `‰` | `झ्` | Half jh |

## Punctuation and Symbols

| Character | Unicode | Description |
|-----------|---------|-------------|
| `Ù` | `;` | Literal semicolon |
| `Ú` | `:` | Literal colon |
| `æ` | `“` | Open curly quote |
| `Æ` | `”` | Close curly quote |
| `.` | `।` | Nepali purna biram |
| `=` | `.` | Literal period |
| `+` | `ं` | Anusvara |
| `F` | `ँ` | Chandrabindu |

## Contextual Rules

The conversion engine applies several post-processing rules to handle the complexities of Devanagari script:

1.  **Reph Positioning**: The character `{` (ර්) is moved before the preceding consonant cluster.
2.  **Matra Reordering**: The short-i matra (`l` / `ि`) is moved after the consonant cluster it modifies.
3.  **M-Transformations**:
    *   `त्रm` → `क्र`
    *   `त्तm` → `क्त`
    *   `उm` → `ऊ`
    *   `भm` → `झ`
    *   `पm` → `फ`
4.  **Vowel Combinations**:
    *   `अ` + `ा` + `े` → `ओ`
    *   `अ` + `ा` + `ै` → `औ`
    *   `अ` + `ा` → `आ`
