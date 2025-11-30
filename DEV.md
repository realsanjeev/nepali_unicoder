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