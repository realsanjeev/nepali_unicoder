import os
import sys

# If running as script, add src to path so absolute imports work
if __name__ == "__main__":
    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
    )

from nepali_unicoder.engine import Engine


class Converter:
    """
    Wrapper around Engine for backward compatibility.
    """

    def __init__(self):
        self.engine = Engine()

    def convert(self, text: str) -> str:
        return self.engine.transliterate(text)


def main():
    if len(sys.argv) < 2:
        # Check if there is stdin
        if not sys.stdin.isatty():
            input_text = sys.stdin.read()
        else:
            print('Usage: python -m nepali_unicoder.convert "your roman text here"')
            print('       or: echo "namaste" | python -m nepali_unicoder.convert')
            return
    else:
        input_text = " ".join(sys.argv[1:])

    converter = Converter()
    result = converter.convert(input_text)
    print(result)


if __name__ == "__main__":
    main()
