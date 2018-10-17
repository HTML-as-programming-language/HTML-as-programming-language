class CodeRange:

    def __init__(self, filedir, filename, line, char, endline, endchar):
        self.dir = filedir
        self.filename = filename
        self.line = line
        self.char = char
        self.endline = endline
        self.endchar = endchar

    def to_json(self):
        return {
            "start": {
                "line": self.line - 1,
                "character": self.char
            },
            "end": {
                "line": self.endline - 1,
                "character": self.endchar
            }
        }

    def in_range(self, line, char=None, filename=None, filedir=None):
        return (
            self.line <= line <= self.endline
            and
            (
                not char
                or
                (
                    line > self.line
                    or
                    char >= self.char
                )
                or
                (
                    line < self.endline
                    or
                    char <= self.endchar
                )
            )
            and
            (
                not filename
                or
                filename == self.filename
            )
            and
            (
                not filedir
                or
                filedir == self.dir
            )
        )
