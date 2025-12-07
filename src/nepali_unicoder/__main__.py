import sys

from nepali_unicoder.convert import Converter


def main():
    if len(sys.argv) < 2:
        # Check if there is stdin
        if not sys.stdin.isatty():
            input_text = sys.stdin.read()
        else:
            print('Usage: python -m nepali_unicoder "your roman text here"')
            print('       or: echo "namaste" | python -m nepali_unicoder')
            return
    else:
        input_text = " ".join(sys.argv[1:])

    converter = Converter()
    result = converter.convert(input_text)
    print(result)


if __name__ == "__main__":
    main()
