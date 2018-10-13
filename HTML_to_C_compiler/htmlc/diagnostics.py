import colorama
from colorama import Fore, Back, Style

"""
On Windows, calling init() will filter ANSI escape sequences out of any text sent to stdout or stderr, 
and replace them with equivalent Win32 calls.
"""
colorama.init()

class Severity:
    ERROR = 1
    WARNING = 2
    INFO = 3
    HINT = 4


class Diagnostic:

    def __init__(self, severity, code_range, message):
        self.severity = severity
        self.code_range = code_range
        self.message = message

    def human_readable(self):
        sev = self.severity
        s = (
            f"{Back.RED}[ERROR]{Style.RESET_ALL}" if sev == Severity.ERROR
            else
            f"{Back.YELLOW}[WARNING]{Style.RESET_ALL}" if sev == Severity.WARNING
            else
            f"{Back.BLUE}[INFO]{Style.RESET_ALL}" if sev == Severity.INFO
            else
            f"{Back.GREEN}[HINT]{Style.RESET_ALL}" if sev == Severity.HINT
            else ""
        )

        s += f" {Style.DIM}{self.code_range.dir}{Style.RESET_ALL}" \
             f"{Fore.CYAN}{self.code_range.filename}{Style.RESET_ALL}" \
             f"\non line {Fore.CYAN}{self.code_range.line}{Style.RESET_ALL} at char {self.code_range.char}"

        mess = self.message
        if sev == Severity.ERROR:
            mess = f"{Fore.RED}{mess}{Style.RESET_ALL}"
        s += "\n\n" + mess + "\n"
        return s


def diagnose(element_tree):

    diagnostics = []

    for el in element_tree:
        diagnostics.extend(el.diagnostics())
        diagnostics.extend(diagnose(el.children))

    return diagnostics


def contains_error(diagnostics):
    for d in diagnostics:
        if d.severity == Severity.ERROR:
            return True
    return False
