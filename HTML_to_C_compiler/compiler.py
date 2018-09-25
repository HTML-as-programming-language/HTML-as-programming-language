from html_parser import HTMLParser
from lexer import Lexer


class Compiler():    # Secrely I am just a transpiler but don't tell onyone

    def __init__(self, uri):
        lexer = Lexer()
        parser = HTMLParser()

        parser.feed(uri, lexer)
        lexed_elements = lexer.elements
        c = self.to_c(lexed_elements)    
        print(c)
                                                    # TODO: this is hardcoded
        file = open("../working-code.c", "w")       # Write the C code to a file
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
