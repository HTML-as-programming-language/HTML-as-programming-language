import sys

from htmlc import utils
from htmlc.html_parser import HTMLParser
from htmlc.diagnostics import diagnose, contains_error
from htmlc.lexer import Lexer
from htmlc.linker import Linker


class Compiler:

    def __init__(self, filepath):
        lexer = Lexer(utils.file_dir(filepath), utils.filename(filepath))
        parser = HTMLParser()

        parser.feed(lexer, filepath=filepath)
        element_tree = lexer.elements

        linker = Linker(element_tree, parser)
        linker.link_external_files()

        diagnostics = diagnose(element_tree)
        diagnostics.extend(linker.diagnostics)
        diagnostics.extend(lexer.diagnostics)

        for d in diagnostics:
            print("-============================-")
            print(d.human_readable())

        if not contains_error(diagnostics):
            print(self.to_c(element_tree))

    def to_c(self, lexed_elements):
        """
        Will return C code based on the Element tree
        """
        c = ""
        for el in lexed_elements:
            el_c = el.to_c()
            if el_c:
                c += el_c
        return c


if __name__ == "__main__":
    print(sys.argv)
    Compiler("../../working-code.html")
