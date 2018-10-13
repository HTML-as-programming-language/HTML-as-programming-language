
class CodeRange:

    def __init__(self, filedir, filename, line, char, endline, endchar):
        self.dir = filedir
        self.filename = filename
        self.line = line
        self.char = char
        self.endline = endline
        self.endchar = endchar
