from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element
from htmlc.utils import hyphenated_to_camel_case


class Truth(Element):
    """"
    HTML: <truth>x</truth>
    C: bool x = true;
    """

    def diagnostics(self):
        return [] if self.data else [Diagnostic(
            Severity.ERROR,
            self.code_range,
            "Please provide bool name like: <truth>i-am-an-idiot</truth>"
        )]

    def to_c(self):
        return "bool {} = true;\n".format(
            hyphenated_to_camel_case(
                "".join(self.data.split())
            )
        )


class Lie(Element):
    """"
    HTML: <lie>y</lie>
    C: bool y = false;
    """

    def diagnostics(self):
        return [] if self.data else [Diagnostic(
            Severity.ERROR,
            self.code_range,
            "Please provide bool name like: <lie>i-am-smart</lie>"
        )]

    def to_c(self):
        return "bool {} = false;\n".format(
            hyphenated_to_camel_case(
                "".join(self.data.split())
            )
        )
