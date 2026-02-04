import argparse
import sys

from nepali_unicoder.convert import Converter


def main():
    parser = argparse.ArgumentParser(
        prog="python -m nepali_unicoder",
        description="Convert Romanized Nepali or Preeti font text to Unicode Devanagari.",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="The text to convert. If omitted, reads from stdin.",
    )
    parser.add_argument(
        "--preeti",
        action="store_true",
        help="Enable Preeti to Unicode conversion mode.",
    )

    args = parser.parse_args()

    # Determine input text
    if args.text:
        input_text = " ".join(args.text)
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
    else:
        parser.print_help()
        return

    mode = "preeti" if args.preeti else "roman"
    converter = Converter(mode=mode)
    result = converter.convert(input_text)
    print(result)


if __name__ == "__main__":
    main()
