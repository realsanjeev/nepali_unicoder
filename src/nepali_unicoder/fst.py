from typing import Dict, Optional, Tuple


class FSTState:
    __slots__ = ("transitions", "is_final", "output")

    def __init__(self):
        self.transitions: Dict[str, "FSTState"] = {}
        self.is_final: bool = False
        self.output: Optional[str] = None


class FST:
    def __init__(self):
        self.root = FSTState()

    def add_mapping(self, input_seq: str, output_seq: str) -> None:
        """
        Add a mapping from input sequence to output sequence.
        """
        node = self.root
        for char in input_seq:
            if char not in node.transitions:
                node.transitions[char] = FSTState()
            node = node.transitions[char]

        node.is_final = True
        node.output = output_seq

    def longest_match(self, text: str) -> Tuple[Optional[str], int]:
        """
        Find the longest matching prefix.
        Returns (output, length_matched).
        """
        node = self.root
        last_output = None
        last_len = 0
        curr_len = 0

        for char in text:
            if char not in node.transitions:
                break
            node = node.transitions[char]
            curr_len += 1

            if node.is_final:
                last_output = node.output
                last_len = curr_len

        return last_output, last_len
