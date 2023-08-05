import argparse
from nlcLatex import load


def main(arguments):
    doc = load(arguments.file)
    doc.process()
    doc.write()
    doc.run_latex()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process .pytex")
    parser.add_argument("file")

    args = parser.parse_args()
    main(args)
