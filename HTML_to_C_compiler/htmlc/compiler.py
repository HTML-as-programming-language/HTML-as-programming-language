import os
import sys
from typing import List

import colorama
from colorama import Fore, Style, Back
from htmlc.elements.element import Element

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

    def __init__(self, filepath: str):
        filedir = utils.file_dir(filepath)
        filename = utils.filename(filepath)
        lexer = Lexer(filedir, filedir)
        parser = HTMLParser()

        parser.feed(lexer, filepath=filepath)
        element_tree = lexer.elements

        linker = Linker(element_tree, parser)
        linker.link_external_files()

        for el in element_tree:
            el.init()
            el.init_children()

        diagnostics = diagnose(element_tree)
        diagnostics.extend(linker.diagnostics)
        diagnostics.extend(lexer.diagnostics)

        for d in diagnostics:
            print("-============================-")
            print(d.human_readable())

        if not contains_error(diagnostics):
            outdir = filedir + "out/"
            outfile = filename.replace('.html', '.c')
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            with open(
                    f"{outdir}{outfile}",
                    "w"
            ) as f:
                f.write(self.to_c(element_tree))
                f.close()
                print(f"{Fore.GREEN}C-code saved in {outdir}{outfile}")

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


# for debugging purposes:
if __name__ == "__main__":
    Compiler("../../working-code.html")


def main():
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

        Compiler(filepath)
    else:
        print(
            f"{Fore.RED}Please give a filepath that ends with .html{Style.RESET_ALL}\n"
            f"For example: {Back.LIGHTBLACK_EX}htmlc my-code.html"
        )
