import re

from htmlc.code_range import CodeRange


class MappedCString:

    class Contributor:

        def __init__(self, element, code_range):
            self.element = element
            self.code_range = code_range

    def __init__(self):
        self.c = ""
        self.contributors = []
        self.line = 0
        self.char = 0
        self.indentation = 0

    def add(self, c, element):

        lines = [
            "\t" * self.indentation + line
            if line else line                   # don't add indent to line without text
            for line in c.split("\n")
        ]
        c = ("\t" * self.indentation + "\n").join(lines)
        self.c += c

        endline = self.line + len(lines) - 1
        endchar = self.char + len(lines[0]) if endline == self.line else len(lines[-1])

        self.contributors.append(
            MappedCString.Contributor(
                element,
                CodeRange(
                    None, None,
                    self.line, self.char,
                    endline, endchar
                )
            )
        )
        self.line = endline
        self.char = endchar

    def indent(self, tabs):
        self.indentation += tabs

    def print_gcc_errors(self, stderr, filename):
        stderr = stderr.decode("utf-8")
        errors = stderr.split(filename + ":")
        for err in errors:

            if not re.match("\d+:\d+:", err):
                # error message does not begin with line:char:
                continue

            line = int(err.split(":")[0])
            char = int(err.split(":")[1])
            element = self.find_element(line, char)

            print(element, err)

    def find_element(self, line, char):
        for cont in self.contributors:
            if cont.code_range.in_range(line, char):
                return cont.element
