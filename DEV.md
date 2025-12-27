# Trie Architecture

A **Trie** (pronounced "try", from re**trie**val), also known as a prefix tree, is a tree-based data structure used to efficiently store and retrieve keys in a dataset of strings. In `nepali_unicoder`, we use a Trie to store mapping rules (e.g., `k` -> `क्`, `ka` -> `क`) to enable fast, greedy transliteration.

## How It Works

### Structure
- **Nodes**: Each node represents a character.
- **Edges**: Links between nodes represent the sequence of characters.
- **Root**: The starting point (empty string).
- **End Marker**: Nodes that complete a valid key are marked as "end nodes" and store the corresponding value (the Devanagari character).

### Operations

#### 1. Insertion
To insert a mapping like `ka` -> `क`:
1. Start at the root.
2. Traverse (or create) the edge for `k`.
3. From the `k` node, traverse (or create) the edge for `a`.
4. Mark the `a` node as an end node and store the value `क`.

#### 2. Longest Prefix Matching (Greedy Match)
This is critical for transliteration. When converting `kha`, we want `kha` -> `ख`, not `k` -> `क्` + `h` -> `ह्` + `a`.
1. Start at the root with the input string `kha...`.
2. Traverse `k`. It's a valid key (`क्`), so remember it as a candidate.
3. Continue to `h`. `kh` is also a valid key (`ख`), so update the candidate.
4. Continue to `a`. `kha` might be a valid key (`ख` + `ा`?).
   - *Note*: In our specific implementation, `kha` maps to `ख` (schwa form).
5. If the next character doesn't match any child, return the last valid candidate found.

## Pros and Cons

### Pros
- **Performance**: Lookup time is $O(L)$ where $L$ is the length of the key (e.g., 3-4 characters), independent of the number of rules. This is much faster than iterating through a list of thousands of rules ($O(N \cdot L)$).
- **Prefix Matching**: Naturally supports finding the longest matching prefix, which is essential for correct transliteration (greedy matching).
- **Predictability**: Performance is consistent regardless of map size.

### Cons
- **Memory Usage**: Tries can consume more memory than a simple hash map because each character is a separate node object with pointers. However, for the size of the Nepali character set, this is negligible.
- **Complexity**: Slightly more complex to implement than a simple dictionary lookup.

## References
- [Trie - Wikipedia](https://en.wikipedia.org/wiki/Trie)
- [Trie - GeeksforGeeks](https://www.geeksforgeeks.org/trie/)

---

# Preeti Conversion Architecture

The Preeti to Unicode conversion uses a **two-phase approach** to handle the complex contextual rules required for accurate conversion.

## Phase 1: Character Mapping

Similar to Roman transliteration, Preeti characters are first mapped using the Trie structure:
- Input: Preeti characters (e.g., `s`, `{`, `l`)
- Trie lookup: Direct character-to-Unicode mapping
- Output: Initial Unicode text (may be incorrect due to lack of context)

Example:
```
Input:  s{
Trie:   s → क, { → {
Output: क{
```

## Phase 2: Post-Processing Rules

After initial mapping, **30 regex-based post-processing rules** are applied in sequence to handle contextual transformations:

### Rule Categories

1. **Invalid Combination Removal**: Remove impossible character sequences
2. **Contextual `m` Handling**: Transform `m` based on surrounding characters
   - `त्रm` → `क्र`, `त्तm` → `क्त`
   - `उm` → `ऊ`, `भm` → `झ`, `पm` → `फ`
3. **Reph (`{`) Positioning**: Move reph to correct position
   - `(.[ािीुूृेैोौंःँ]*?){` → `{\1` (move before matras)
   - `{` → `र्` (final conversion)
4. **Matra Reordering**: Reposition vowel signs
   - `ि((.्)*[^्])` → `\1ि` (move short i after consonant)
5. **Anusvara/Chandrabindu**: Move to end of character cluster
6. **Duplicate Removal**: Remove duplicate matras
7. **Visarga Handling**: Special handling for visarga at line start
8. **Special Combinations**: Handle specific character combinations
9. **Vowel Combinations**: Combine vowel signs with independent vowels

### Example Flow

```
Input:     s{
Phase 1:   क{
Rule 3.3:  {क  (move { before matras)
Rule 3.4:  र्क (convert { to र्)
Output:    र्क
```

## Why Two Phases?

Preeti font is a **visual encoding** where characters don't follow Unicode's logical ordering. For example:
- Reph (`र्`) appears **above** a consonant but is typed **after** it in Preeti
- Short i matra (`ि`) appears **before** a consonant but is typed **after** it in Preeti

The post-processing phase reorders these characters to match Unicode's logical structure.

## Performance Considerations

- **Phase 1**: O(L) where L is input length (Trie lookup)
- **Phase 2**: O(L × R) where R is number of rules (30 regex passes)
- Total: Still very fast for typical text lengths