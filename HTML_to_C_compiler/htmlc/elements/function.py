from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element
from htmlc.utils import hyphenated_to_camel_case, indent


class Param(Element):

    def __init__(self):
        super().__init__()
        self.name = None
        self.type = None

    def init(self):
        self.type = self.attributes.get("type", {}).get("val")
        for key in self.attributes:
            if key != "type":
                self.name = key
                break

    def diagnostics(self):
        return [] if self.type else [Diagnostic(
            Severity.ERROR,
            self.code_range,
            "Unkown param type"
        )]


class Def(Element):
    """"
    HTML:
    <def functionname></def>
    <def multiply returns="int"></def>

    C:
    void functionname() {}
    int multiply() {}
    """

    def diagnostics(self):
        d = []
        for el in self.children:
            if not isinstance(el, Param):
                continue
            if not el.name:
                d.append(Diagnostic(Severity.ERROR, el.code_range, "Param without name"))
        return d


    def to_c(self):
        return_type = self.attributes.get("returns", {}).get("val", "void")
        func_name = None
        for key in self.attributes:
            if key != "returns":
                func_name = hyphenated_to_camel_case(key)

        params = []

        for el in self.children:
            if el.tagname != "param":
                continue
            param_name = el.name
            param_type = el.type
            params.append(param_type + " " + param_name)

        c = "\n\n{} {}({})".format(
            return_type,
            func_name,
            ", ".join(param for param in params)
        ) + " {\n"

        c += indent(self.children_to_c(), 1)
        c += "}\n"
        return c
