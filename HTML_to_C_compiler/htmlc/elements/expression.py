from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element


class Expression(Element):
    """"
    HTML:
    <expression x="a > 50">
        <ya-really>
            <!-- if-code here -->
        </ya-really>

        <maybe x="a < 10">
            <!-- else-if code here -->
        </maybe>

        <no-wai>
            <!-- else code here -->
        </no-wai>
    </expression>

    C:
    if (a > 50){
        //code goes here
    }
    else if (a < 10) {
        //else-if code here
    }
    else {
        //else code here
    }
    """

    def __init__(self):
        super().__init__()
        self.x = None

    def init(self):
        self.x = self.attributes.get("x", {}).get("val")

    def diagnostics(self):
        return [] if self.x else [Diagnostic(
            Severity.ERROR,
            self.code_range,
            "Expression element without x attribute"
        )]

    def to_c(self, mapped_c):
        # 'if' body:
        mapped_c.add(
            f"if ({self.x})" + " {\n",
            self
        )
        mapped_c.indent(1)
        for child in self.children:
            if not isinstance(child, YaReally):
                continue
            child.to_c(mapped_c)
        mapped_c.indent(-1)
        mapped_c.add("}\n", self)

        # 'else-if' bodies:
        for child in self.children:
            if isinstance(child, Maybe):
                child.to_c(mapped_c)

        # 'else' body:
        mapped_c.add(
            "else {\n",
            self
        )
        mapped_c.indent(1)
        for child in self.children:
            if isinstance(child, NoWai):
                child.to_c(mapped_c)
                break
        mapped_c.indent(-1)
        mapped_c.add("}\n", self)


class ExpressionChild(Element):

    def to_c(self, mapped_c):
        self.children_to_c(mapped_c)

    def diagnostics(self):
        return [] if isinstance(self.parent, Expression) else [
            Diagnostic(
                Severity.ERROR,
                self.code_range,
                "{} element found outside of expression element".format(self.tagname)
            )
        ]


class YaReally(ExpressionChild):
    pass


class Maybe(ExpressionChild):

    def __init__(self):
        super().__init__()
        self.x = None

    def init(self):
        self.x = self.attributes.get("x", {}).get("val")

    def diagnostics(self):
        d = super().diagnostics()
        if not self.x:
            d.append(Diagnostic(
                Severity.ERROR,
                self.code_range,
                "Maybe element found without x-attribute"
            ))
        return d

    def to_c(self, mapped_c):
        mapped_c.add(f"else if ({self.x})" + " {\n", self)
        mapped_c.indent(1)
        self.children_to_c(mapped_c)
        mapped_c.indent(-1)
        mapped_c.add("}\n\n", self)


class NoWai(ExpressionChild):
    pass
