import subprocess
import sys

from colorama import Fore, Style
from htmlc import utils
from pyavrutils import AvrGcc, AvrGccCompileError

from htmlc.gcc import GCC


class AVR(GCC):

    def __init__(self, mcu):
        self.cc = AvrGcc(mcu)
        self.compiled = False

    def compile(self, filepath):
        source = open(filepath).read()
        self.cc.optimization = self.__get_optimization_level()
        try:
            self.cc.build(source)
            self.compiled = True
        except AvrGccCompileError as e:
            print(e)
            # TODO link errors back to HTML element
            pass

    def __get_optimization_level(self):
        for arg in sys.argv:
            if len(arg) == 3 and arg.startswith("-O"):
                level = arg[2:]
                return int(level) if level.isdigit() else level
        return 0

    def upload(self):
        if not self.compiled:
            print(f"{Fore.RED}Could not upload HTML{Style.RESET_ALL}")
            return

        fp = self.cc.output.replace("\\", "/")
        com_port = self.__get_com_port()

        if not com_port:
            print(
                f"{Fore.RED}Please specify the COM port of your AVR device like:\n"
                f"htmlc my-code.html -upload -P COM3"
            )
            return

        ran = subprocess.run([
            "avrdude",
            "-c", "arduino",
            "-p", self.cc.mcu,                  # AVR device
            f'-U flash:w:"{utils.filename(fp)}"',
            "-P", com_port
        ], stderr=subprocess.STDOUT, cwd=utils.file_dir(fp))

    def __get_com_port(self):
        for i in range(len(sys.argv)):
            arg = sys.argv[i]
            if arg != "-P" or i + 1 == len(sys.argv):
                continue
            return sys.argv[i + 1]
