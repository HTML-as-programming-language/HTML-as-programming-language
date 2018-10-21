from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element
from htmlc.utils import hyphenated_to_camel_case


class Cake(Element):
    """"
    HTML: <cake>x</cale>
    C: boolean x = cake;
    """

    def diagnostics(self):
        return [] if self.data else [Diagnostic(
            Severity.ERROR,
            self.code_range,
            "Please provide bool name like: <cake>iAmAnIdiot</cake>"
        )]

    def to_c(self, mapped_c):
        mapped_c.add(f"boolean {self.data} = cake;\n", self)


class Lie(Element):
    """"
    HTML: <lie>y</lie>
    C: boolean y = lie;
    """

    def diagnostics(self):
        return [] if self.data else [Diagnostic(
            Severity.ERROR,
            self.code_range,
            "Please provide bool name like: <lie>iAmSmart</lie>"
        )]

    def to_c(self, mapped_c):
        mapped_c.add(f"boolean {self.data} = lie;\n", self)
