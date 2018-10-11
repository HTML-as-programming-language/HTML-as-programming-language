from elements.element import Element
from utils import hyphenated_to_camel_case, indent


class Param(Element):

    def get_name(self):
        for key in self.attributes:
            if key != "type":
                return key
        raise Exception(
            "Param with no name on line " + self.line
        )

    def get_type(self):
        typee = self.attributes.get("type", {}).get("val")
        if not typee:
            raise Exception("Param without a type on line {}".format(self.line))
        return typee


class Def(Element):
    """"
    HTML:
    <def functionname></def>
    <def multiply returns="int"></def>

    C:
    void functionname() {}
    int multiply() {}
    """

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
            param_name = el.get_name()
            param_type = el.get_type()
            params.append(param_type + " " + param_name)

        c = "\n\n{} {}({})".format(
            return_type,
            func_name,
            ", ".join(param for param in params)
        ) + " {\n"

        c += indent(self.children_to_c(), 1)
        c += "}\n"
        return c
