import os
import sys

import colorama
from colorama import Fore, Style, Back

from htmlc import utils
from htmlc.html_parser import HTMLParser
from htmlc.diagnostics import diagnose, contains_error
from htmlc.lexer import Lexer
from htmlc.linker import Linker

"""
On Windows, calling init() will filter ANSI escape sequences out of any text sent to stdout or stderr, 
and replace them with equivalent Win32 calls.
"""
colorama.init()


class Compiler:

    def __init__(self, filepath):
        self.dir = utils.file_dir(filepath)
        self.filename = utils.filename(filepath)
        self.diagnostics = None
        self.lexer = Lexer(self.dir, self.filename)
        parser = HTMLParser()

        parser.feed(self.lexer, filepath=filepath)
        self.element_tree = self.lexer.elements

        self.linker = Linker(self.element_tree, parser)
        self.linker.link_external_files()

        self.__init_elements()
        self.__diagnose()

    def __init_elements(self):
        for el in self.element_tree:
            el.init()
            el.init_children()

    def __diagnose(self):
        self.diagnostics = diagnose(self.element_tree)
        self.diagnostics.extend(self.linker.diagnostics)
        self.diagnostics.extend(self.lexer.diagnostics)

        for d in self.diagnostics:
            print("-============================-")
            print(d.human_readable())

    def __to_c(self):
        """
        Will return C code based on the Element tree
        """
        c = ""
        for el in self.element_tree:
            el_c = el.to_c()
            if el_c:
                c += el_c
        return c

    def save_to_c_file(self):
        if not contains_error(self.diagnostics):
            outdir = self.dir + "out/"
            outfile = self.filename.replace('.html', '.c')
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            with open(
                    f"{outdir}{outfile}",
                    "w"
            ) as f:
                f.write(self.__to_c())
                f.close()
                print(f"{Fore.GREEN}C-code saved in {outdir}{outfile}")
        else:
            print(f"{Fore.RED}Could not transpile to C because HTML-code is invalid{Style.RESET_ALL}")


# for debugging purposes:
if __name__ == "__main__":
    if sys.version_info < (4,): # python version < 3
        print(
            f"You are running Python version {sys.version_info[0]}.{sys.version_info[1]}\n"
            "HTMLC requires Python 3.\n"
            "If you have Python 3 try:\n"
            "pip3 install HTML-as-programming-language"
        )
    Compiler("../../working-code.html").save_to_c_file()


def main():
    if sys.version_info < (4,): # python version < 3
        print(
            f"You are running Python version {sys.version_info[0]}.{sys.version_info[1]}\n"
            "HTMLC requires Python 3.\n"
            "If you have Python 3 try:\n"
            "pip3 install HTML-as-programming-language"
        )
        return

    filepath = None
    for arg in sys.argv:
        if arg.endswith(".html"):
            filepath = arg
    if filepath:
        try:
            open(filepath)
        except FileNotFoundError:
            print(f"{Fore.RED}File not found: {filepath}")
            return

        Compiler(filepath).save_to_c_file()
    else:
        print(
            f"{Fore.RED}Please give a filepath that ends with .html{Style.RESET_ALL}\n"
            f"For example: {Back.LIGHTBLACK_EX}htmlc my-code.html{Style.RESET_ALL}"
        )
