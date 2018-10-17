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
