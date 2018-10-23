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
        return [] if self.type or not isinstance(self.parent, Def) else [Diagnostic(
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

    def to_c(self, mapped_c):
        return_type = self.attributes.get("returns", {}).get("val", "void")
        func_name = None
        for key in self.attributes:
            if key != "returns":
                func_name = hyphenated_to_camel_case(key)

        mapped_c.add(f"\n{return_type} {func_name}(", self)

        first_param = True
        for el in self.children:
            if el.tagname != "param":
                continue
            param_name = el.name
            param_type = el.type
            if not first_param:
                mapped_c.add(", ", self)
            mapped_c.add(f"{param_type} {param_name}", el)
            first_param = False

        mapped_c.add(") {\n", self)
        mapped_c.indent(1)
        self.children_to_c(mapped_c)
        mapped_c.indent(-1)
        mapped_c.add("}\n\n", self)
