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
        self.operator = "="

    def init(self):
        for key in self.attributes:
            self.var_name = key

        self.val = (
                self.get_inner_value()
                or
                self.attributes[self.var_name].get("val") if self.var_name else None
        )

    def diagnostics(self):
        d = []
        if not self.var_name:
            d.append(
                Diagnostic(
                    Severity.ERROR,
                    self.code_range,
                    f"No variable name given (for example: <{self.tagname} varName>123</assign>)"
                )
            )
        elif not self.val:
            d.append(
                Diagnostic(
                    Severity.ERROR,
                    self.code_range,
                    f"Usage: <{self.tagname} {self.var_name}>something</{self.tagname}>"
                )
            )
        return d

    def to_c(self, mapped_c):
        mapped_c.add(f"{self.var_name} {self.operator} ", self)
        if isinstance(self.val, Element):
            self.val.to_c(mapped_c)
        else:
            mapped_c.add(f"{self.val}", self)
        mapped_c.add(";\n", self)


class Add(Assign):
    def __init__(self):
        super().__init__()
        self.operator = "+="


class Minus(Assign):
    def __init__(self):
        super().__init__()
        self.operator = "-="


class AndBits(Assign):
    def __init__(self):
        super().__init__()
        self.operator = "&="


class OrBits(Assign):
    def __init__(self):
        super().__init__()
        self.operator = "|="


class XorBits(Assign):
    def __init__(self):
        super().__init__()
        self.operator = "^="


class Multiply(Assign):
    def __init__(self):
        super().__init__()
        self.operator = "*="


class Divide(Assign):
    def __init__(self):
        super().__init__()
        self.operator = "/="


class Modulo(Assign):
    def __init__(self):
        super().__init__()
        self.operator = "%="

