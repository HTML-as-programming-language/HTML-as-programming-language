from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element


class Assign(Element):
    """"
    HTML: <assign a>5</assign>
    C: a = 5;

    or

    HTML: <assign a><have nr0 of>myPile</have></assign>
    C: a = myPile[0];
    """
    def __init__(self):
        super().__init__()
        self.var_name = None
        self.is_value_wrapper = True
        self.val = None

    def init(self):
        for key in self.attributes:
            self.var_name = key

        self.val = self.get_inner_value()

    def diagnostics(self):
        d = []
        if not self.var_name:
            d.append(
                Diagnostic(
                    Severity.ERROR,
                    self.code_range,
                    "No variable name given (for example: <assign varName>123</assign>)"
                )
            )
        elif not self.val:
            d.append(
                Diagnostic(
                    Severity.ERROR,
                    self.code_range,
                    "Cannot assign nothing to {}".format(self.var_name)
                )
            )
        return d

    def to_c(self, mapped_c):
        mapped_c.add(f"{self.var_name} = ", self)
        if isinstance(self.val, Element):
            self.val.to_c(mapped_c)
        else:
            mapped_c.add(self.val, self)
        mapped_c.add(";\n", self)
