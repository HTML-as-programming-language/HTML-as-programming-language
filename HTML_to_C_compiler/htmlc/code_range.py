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
