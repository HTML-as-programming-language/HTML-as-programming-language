from htmlc import utils
from htmlc.html_parser import HTMLParser
from htmlc.lexer import Lexer
from htmlc.linker import Linker


class Compiler:

    def __init__(self, filepath):
        lexer = Lexer(utils.file_dir(filepath), utils.filename(filepath))
        parser = HTMLParser()

        parser.feed(filepath, lexer)
        element_tree = lexer.elements

        linker = Linker(element_tree, parser)
        linker.link_external_files()

        c = self.to_c(element_tree)
        print(c)
                                                    # TODO: this is hardcoded
        file = open("../../working-code.c", "w")       # Write the C code to a file
        file.write(c)
        file.close()

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


compiler = Compiler("../working-code.html")   # Construct the compiler


# TODO: litle commandline program that gets flags from the user

# compile to C
# compile to assembly

# compile and run
# compile and print result in commandline
