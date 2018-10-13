from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element
from htmlc.utils import hyphenated_to_camel_case


class Var(Element):
    """"
    HTML:

    <var b=6/>
    <var aString="hello"/>
    <var aChar='b'/>

    C:
    int b = 6;
    String aString = "hello";
    char aChar = 'b';
    """

    def __init__(self):
        super().__init__()
        self.type = None
        self.var_name = None
        self.attr = None

    def init(self):
        for key in self.attributes:
            if key == "type":
                continue
            self.var_name = hyphenated_to_camel_case(key)
            self.attr = self.attributes[key]

        self.type = self.attributes.get("type", {}).get("val")
        if self.type is None:  # user did not provide type like <var x=y type="int"/>
            self.type = (self.attr["type"] or "unknown") if self.attr else "unknown"

    def diagnostics(self):
        d = []
        if not self.var_name:
            d.append(Diagnostic(
                Severity.ERROR,
                self.code_range,
                "No variable name defined"
            ))
        if not self.type or self.type == "unknown":
            d.append(Diagnostic(
                Severity.ERROR,
                self.code_range,
                "Unknown variable type"
                "\nPlease provide a type in the type attribute like <var x=y type='int'/>"
            ))
        return d


    def to_c(self):
        val = self.attr["val"]
        if self.type == "String":
            val = '"{}"'.format(val)
        elif self.type == "char":
            val = "'{}'".format(val)

        return "{} {} = {};\n".format(self.type, self.var_name, val)
