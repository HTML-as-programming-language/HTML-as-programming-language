from colorama import Fore, Style

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
        s = ""

        sev = self.severity
        s += "[" + (
            f"{Fore.RED}ERROR{Style.RESET_ALL}" if sev == Severity.ERROR
            else
            f"{Fore.YELLOW}WARNING{Style.RESET_ALL}" if sev == Severity.WARNING
            else
            f"{Fore.BLUE}INFO{Style.RESET_ALL}" if sev == Severity.INFO
            else
            f"{Fore.GREEN}HINT{Style.RESET_ALL}" if sev == Severity.HINT
            else ""
        ) + "]"

        s += f" {self.code_range.dir}{Fore.CYAN}{self.code_range.filename}{Style.RESET_ALL}" \
             f"\non line {Fore.CYAN}{self.code_range.line}{Style.RESET_ALL} at char {self.code_range.char}"

        s += "\n" + self.message + "\n"
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
