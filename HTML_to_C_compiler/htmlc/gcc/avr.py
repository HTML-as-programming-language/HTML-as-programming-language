import subprocess
import sys

from colorama import Fore, Style
from htmlc import utils

from htmlc.gcc.gcc import GCC


class AVR(GCC):

    def __init__(self, mcu):
        self.mcu = mcu
        self.compiled = False
        self.hexfile = None
        self.dir = None

    def compile(self, filepath, mapped_c):
        filename = utils.filename(filepath)
        self.dir = utils.file_dir(filepath)
        name = filename[:-2]    # remove '.c'
        proc = subprocess.run([
            "avr-gcc",
            "-mmcu=" + self.mcu,
            filename,
            "-o", name + ".o",
            "-O3"
        ], cwd=self.dir, stderr=subprocess.PIPE)

        if proc.returncode:
            mapped_c.print_gcc_errors(proc.stderr, filename)
            return

        self.hexfile = name + ".hex"
        proc = subprocess.run([
            "avr-objcopy",
            "-j", ".text", "-j", ".data",
            "-O", "ihex",
            name + ".o",
            self.hexfile
        ], cwd=self.dir)
        self.compiled = not proc.returncode

    def upload(self):
        if not self.compiled:
            print(f"{Fore.RED}Could not upload HTML{Style.RESET_ALL}")
            return

        com_port = self.__get_com_port()

        if not com_port:
            print(
                f"{Fore.RED}Please specify the COM port of your AVR device like:\n"
                f"htmlc my-code.html -upload -P COM3{Style.RESET_ALL}"
            )
            return

        subprocess.run([
            "avrdude",
            "-c", "arduino",
            "-p", self.mcu,
            "-P", com_port,
            "-U", f'flash:w:{self.hexfile}'
        ], cwd=self.dir)


    def __get_com_port(self):
        for i in range(len(sys.argv)):
            arg = sys.argv[i]
            if arg != "-P" or i + 1 == len(sys.argv):
                continue
            return sys.argv[i + 1]
