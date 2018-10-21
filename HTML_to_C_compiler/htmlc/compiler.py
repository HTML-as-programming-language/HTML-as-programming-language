import os
import sys

import colorama
from colorama import Fore, Style, Back

from htmlc import utils
from htmlc.c_linker import CLinker
from htmlc.gcc.avr import AVR
from htmlc.gcc.gcc import GCC
from htmlc.html_parser import HTMLParser
from htmlc.diagnostics import diagnose, contains_error
from htmlc.lexer import Lexer
from htmlc.linker import Linker
from htmlc.mapped_c_string import MappedCString

"""
On Windows, calling init() will filter ANSI escape sequences out of any text sent to stdout or stderr, 
and replace them with equivalent Win32 calls.
"""
colorama.init()


class Compiler:

    def __init__(self, filepath):
        self.dir = utils.file_dir(filepath)
        self.filename = utils.filename(filepath)
        self.outdir = None
        self.outfile = None
        self.diagnostics = None
        self.mapped_c = None
        self.lexer = Lexer(self.dir, self.filename)
        parser = HTMLParser()

        parser.feed(self.lexer, filepath=filepath)
        self.element_tree = self.lexer.elements

        self.linker = Linker(self.element_tree, parser)
        self.linker.link_external_files()

        self.c_linker = CLinker(self.element_tree, self.lexer.doctype)

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

    def __is_avr(self):
        return self.lexer.doctype.startswith("avr/") if self.lexer.doctype else False

    def __mcu(self):
        return None if not self.__is_avr() else self.lexer.doctype.split("avr/")[1]

    def __to_c(self):
        """
        Will return C code based on the Element tree
        """
        self.mapped_c = MappedCString()
        self.mapped_c.add(self.c_linker.get_includes_code(), None)
        for el in self.element_tree:
            el.to_c(self.mapped_c)
        return self.mapped_c.c

    def save_to_c_file(self):
        if not contains_error(self.diagnostics):
            self.outdir = outdir = self.dir + "out/"
            self.c_linker.save_htmlc_files(outdir)
            self.outfile = outfile = self.filename.replace('.html', '.c')
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            with open(
                    f"{outdir}{outfile}",
                    "w"
            ) as f:
                f.write(
                    self.__to_c()
                )
                f.close()
                print(f"{Fore.GREEN}C-code saved in {outdir}{outfile}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}Could not transpile to C because your HTML-code sucks{Style.RESET_ALL}")
            return False

    def gcc(self):
        if self.__is_avr():
            # AVR GCC
            gcc_compiler = AVR(self.__mcu())
        else:
            # default GCC
            gcc_compiler = GCC()

        gcc_compiler.compile(self.outdir + self.outfile, self.mapped_c)
        return gcc_compiler

    def avr_gcc_and_upload(self):
        if not self.__is_avr():
            print(
                f"{Fore.RED}Cannot upload a non-AVR html file to an AVR microcontroller\n"
                "Your html file should include a <!DOCTYPE avr/*microcontroller-name-here*> tag\n\n"
                "If you use an Arduino UNO for example: <!DOCTYPE avr/atmega328p>\n"
                f"Read the wiki for more info.{Style.RESET_ALL}"
            )
            return
        self.gcc().upload()


# for debugging purposes:
if __name__ == "__main__":
    compiler = Compiler("../../working-code/pins.html")
    if "-P" not in sys.argv:
        sys.argv.extend(["-P", "COM3"])     # lol set default AVR upload port to COM3
    if compiler.save_to_c_file():
        compiler.gcc()


def main():
    # CHECK PYTHON VERSION
    if sys.version_info < (3,):
        print(
            f"You are running Python version {sys.version_info[0]}.{sys.version_info[1]}\n"
            "HTMLC requires Python 3.\n"
            "If you have Python 3 try:\n"
            "pip3 install HTML-as-programming-language"
        )
        return

    # GET FILEPATH
    filepath = None
    for arg in sys.argv:
        if arg.endswith(".html"):
            filepath = arg
    if not filepath:
        print(
            f"{Fore.RED}Please give a filepath that ends with .html{Style.RESET_ALL}\n"
            f"For example: {Back.LIGHTBLACK_EX}htmlc my-code.html{Style.RESET_ALL}"
        )
        return

    # CHECK IF FILE EXISTS
    try:
        open(filepath)
    except FileNotFoundError:
        print(f"{Fore.RED}File not found: {filepath}")
        return

    # TRANS/COM PILE HTML TO C-code
    compiler = Compiler(filepath)
    saved_to_c = compiler.save_to_c_file()

    if not saved_to_c:
        return

    # compile the C-code with AVR-GCC & upload
    if "-upload" in sys.argv:
        compiler.avr_gcc_and_upload()

    # compile the C-code with (AVR-)GCC only
    elif "-compile" in sys.argv:
        compiler.gcc()

    # Don't compile the C-code with GCC
    else:
        pass
