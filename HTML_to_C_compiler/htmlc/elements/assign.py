from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element


class Assign(Element):
    """"
    HTML: <assign a>5</assign>
    C: a = 5
    """
    def __init__(self):
        super().__init__()
        self.var_name = None

    def init(self):
        for key in self.attributes:
            self.var_name = key

    def diagnostics(self):
        d = []
        if not self.var_name:
            d.append(
                Diagnostic(
                    Severity.ERROR,
                    self.code_range,
                    "No variable name given (for example: <assign var-name>123</assign>)"
                )
            )
        elif not self.data:
            d.append(
                Diagnostic(
                    Severity.ERROR,
                    self.code_range,
                    "Cannot assign nothing to {}".format(self.var_name)
                )
            )
        return d

    def to_c(self):
        return "{} = {};\n".format(self.var_name, self.data.strip())
