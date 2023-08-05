import argparse

from nlcLatex.document import Document

NAMES = (
    "chapter",
    "section",
    "subsection",
    "subsubsection",
    "paragraph",
    "subparagraph",
    "part",
)
LEVELS = {NAMES[i]: i for i in range(-1, 6)}


def get_level(current, delta=0):
    if isinstance(current, int):
        if not -1 <= current <= 5:
            raise IndexError(current)
    else:
        if current == "-1" or current.isdecimal():
            return get_level(int(current), delta)
        else:
            try:
                current = LEVELS[current.split("{", 1)[0].strip(" \\").lower()]
            except KeyError:
                raise KeyError(current)
    current += delta
    if not -1 <= current <= 5:
        raise IndexError(current)
    return NAMES[current]


def load(path):
    return Document(path)


def latex_safe(s, visiblespace=False):
    # split to preserve existing backslash
    w = s.split("\\")
    for c in "&%$#_{}":
        cr = "\\{}".format(c)
        w = [i.replace(c, cr) for i in w]
    for c in (
        ("\u200B", "[U+200B]"),
        ("\u25CF", "[U+25CF]"),
        ("\u00D7", "[U+00D7]"),
        ("\u2192", "$\\rightarrow$"),
    ):
        w = [i.replace(c[0], c[1]) for i in w]
    if visiblespace:
        w = [i.replace(' ', '\\textvisiblespace{}') for i in w]
    w = [i.replace("~", "\\textasciitilde{}") for i in w]
    w = [i.replace("^", "\\textasciicircum{}") for i in w]
    result = "\\textbackslash{}".join(w)
    return result


def index_page(level=1):
    return (
        "\\clearpage\n\\phantomsection\n\\addcontentsline{toc}"
        f"{{{get_level(level)}}}"
        "{\\protect{\\numberline{}}Index}\n\\printindex"
    )


class ArgParser(argparse.ArgumentParser):
    def parse_args(self, *args, **kwargs):
        name_space = super(ArgParser, self).parse_args(*args, **kwargs)
        return argparse.Namespace(**{i[0]: i[1][1:-1] for i in name_space._get_kwargs()})
