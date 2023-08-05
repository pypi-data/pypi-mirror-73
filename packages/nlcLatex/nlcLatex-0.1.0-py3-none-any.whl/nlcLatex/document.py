import pathlib
import re
import subprocess
import sys


RE_INPUT_INCLUDE = re.compile(r"(include|input)(\[.*\])?{(.*?)(}.*)")


class Document:
    def __init__(self, file_name):
        self.path = pathlib.Path(file_name).resolve()
        self.buffer = []
        self._load()
        if self.buffer[0].startswith(r"\documentclass"):
            matches = re.search(r"{(.+?)}", self.buffer[0])
            if not matches:
                raise RuntimeError("LaTeX Documentclass not found")
            self.document_class = matches.group(1)
        else:
            self.document_class = None

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line.startswith("%"):
                    self.buffer.append(line)

    def process(self):
        temp = []
        for line in self.buffer:
            if r"\input" in line or r"\include" in line:
                temp.append(self.process_input_include(line))
            else:
                temp.append(line)
        self.buffer = temp

    def process_input_include(self, line):
        result = ""
        for i in line.split("\\"):
            m = RE_INPUT_INCLUDE.match(i)
            if m is None:
                # no match, just add current item plus separator
                result += i + "\\"
            else:
                # group 1: either "input" or "include"
                # group 2: parameters (in [ ] ) either [a b c] or [a][b][c]
                # group 3: filename
                # group 4: remainder including "}"
                path = self.path.parent / pathlib.Path(f"{m.group(3)}.pytex")
                if path.exists():
                    doc = Document(path)
                    doc.process()
                    doc.write()
                else:
                    path = self.path.parent / pathlib.Path(f"{m.group(3)}.py")
                    if path.exists():
                        param = [sys.executable, str(path)]
                        if m.group(2):
                            temp = m.group(2)[1:-1]
                            temp = temp.split("][") if "]" in temp else temp.split()
                            param.extend([f'"{i}"' for i in temp])
                        subprocess.run(param,  stderr=subprocess.PIPE)
                # add without possible parameters
                result += f"{m.group(1)}{{{m.group(3)}{m.group(4)}"
        return result

    def write(self):
        with open(
            f"{self.path.parent / self.path.stem}.tex", "w", encoding="utf-8"
        ) as f:
            f.write("\n".join(self.buffer))

    def run_latex(self):
        self.run_latex_tex()
        self.run_latex_gls()
        self.run_latex_idx()
        for i in range(5):
            if not self.run_latex_tex():
                break

    def run_latex_tex(self):
        response = subprocess.run(
            [
                "pdflatex",
                "-synctex=1",
                "-interaction=nonstopmode",
                f"{self.path.stem}.tex",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.path.parent,
        )
        return response.returncode

    def run_latex_idx(self):
        subprocess.run(
            ["texindy", f"{self.path.stem}.idx"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.path.parent,
        )

    def run_latex_gls(self):
        subprocess.run(
            ["makeglossaries", f"{self.path.stem}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.path.parent,
        )
