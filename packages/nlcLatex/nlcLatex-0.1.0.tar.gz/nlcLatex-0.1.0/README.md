# nlcLatex

*This this the very first version. I removed logging to keep this very light and small. 
Logging and error responses will be added later.*

Tools to create Latex Documents.

Processes files with extension `.pytex` 
inside any include / input is checked if 

- `.pytex` exists -> process this file
- `.py` exists -> run as python. The script is expected to write a 
  `.tex` file with the same name.


### Process:

1. load file and create / return document

    `doc = nlcLatex.load(<filename>)`

2. process the includes within document
    
    `doc.process()`
    
3. write LaTeX file

    `doc.write()`
    
4. run `pdflatex`

    `doc.run_latex()`
    
`nlcLatex.process` takes the name of a `.pytex`-file and executes the steps mentioned above.

### Providing Parameters (for Python scripts)

Parameters can be provided with in the respective `\inclucde` or `\input` statement in two formats:

- `\input[p1][p2][with space]{script-name}`
- `\input[p1 p2 p3]{script-name}`

The first form allows parameters with spaces, the second form is split at the whitespace to
separate the parameters.

Note: I typically use the first parameter to signify the LaTeX section level, numerical from -1 to 5, or using the 
respective names (e.g. 'chapter').

## Public Interface

Functions:

### `nlcLatex.load(<file-name>)` or `nlcLatex.Document(<file-name>)`

Expects a `.pytex`-file that conforms to a regular LaTeX document with the possible 
exception of `\include` and `\input` format.

Returns an instance of `nlcLatex.Document`

### `nlcLatex.get_level(<level>, delta=0)` 

Returns the respective Latex-Name of the sectioning level, can be provided as integer or 
name. Delta allows to calculate up or down.

|int|name|
|:---:|----|
|-1 | part |
| 0 | chapter |
| 1 | section |
| 2 | subsection |
| 3 | subsubsection |
| 4 | paragraph |
| 5 | subparagraph |

Tip: Might be used like this:

`f'\\{get_level(current, 1)}[Toc-Entry]{{Text}}`

### `nlcLatex.latex_safe(<string>, visiblespace=False)`

Returns a string that has special Latex-characters replaced with their respective escape sequences:

|char|replacement| |char|replacement|
|:---:|:---:|:---:|:---:|:---:|
| & | \\&  | | %  | \\% |
| $ | \\$  | | #  | \\# |
| _ | \\_ | | {  | \\{  |
| } | \\} | | | |
| Unicode Character 'ZERO WIDTH SPACE'| [U+200B] | | &#9679; | [U+25CF] |
| &#215; | [U+00D7] | | &#8594; | $\\rightarrow$ |
| ~ | \\textasciitilde{} | | ^ | \\textasciicircum{} |

If `visiblespace=True`, spaces will be replaced with `\textvisiblespace{}` (&#9251;)

### `nlcLatex.index_page(level=1)`

Returns string to insert toc-entry for Index and issues `\printindex`

### `nlcLatex.ArgParser`

Wrapper around `argparse.ArgumentParser` to remove double quotes around parameters (they are required to protect spaces).

## Example

The following files can be stored in the same directory and show an example:

### `example01.py` 

```python
import pathlib

from nlcLatex import get_level, latex_safe, ArgParser


def main(args):
    path = pathlib.Path(__file__)
    with open(path.with_suffix(".tex"), "w", encoding="utf8") as f:
        f.write("\\" f"{get_level(args.level)}" "{Test}\n\n")
        f.write(latex_safe(args.text, visiblespace=True))


if __name__ == "__main__":
    parser = ArgParser()

    parser.add_argument("level")
    parser.add_argument("text")

    main(parser.parse_args())
```

### `report.pytex`

```latex
\documentclass{article}
\usepackage[utf8]{inputenc}

\begin{document}

    \title{Example Article}
    \author{Automated with \texttt{nlcLatex}}

    \maketitle

    \tableofcontents

    \vfill

    \section{Executive Summary}

    \input[subsection][A parameter]{example01}

    \section{Background}

\end{document}
```