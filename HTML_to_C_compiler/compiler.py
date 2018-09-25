from lexer import Lexer
from utils import camel_case_to_hyphenated


class Compiler():    # Secrely I am just a transpiler but don't tell onyone

    def __init__(self, uri):
        self.isArduino = False          # geeft aan of de code moet worden gecompileerd naar een .ino bestand voor de Arduino
                                        # TODO: Change to flag

        lexer = Lexer()                 # TODO: the lexer now inherits from the parser. The Lexer should instead take in a parser
        lexer.feed(uri)
        lexed_elements = lexer.get_elements()   # TODO: check performance of throwing this around
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

            #TODO make the function to_ino to compile to .ino file format (takes over from to_c
            #if the HTML file has <include> arduino </include> in it, the HTML code must be compiled to a .ino file, #include <arduino> is not written to the .ino file
            if el_c == "#include <arduino>":
                self.isArduino = True
                continue

            if el_c:
                c += el_c

        return c






compiler = Compiler("../working-code.html")   # Construct the compiler






# TODO: litle commandline program that gets flags from the user

# compile to C
# compile to assembly

# compile and run
# compile and print result in commandline