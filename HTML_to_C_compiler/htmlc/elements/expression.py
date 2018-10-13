from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element
from htmlc.utils import indent


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

    def to_c(self):
        # 'if' body:
        c = "if ({})".format(self.x) + " {\n"
        for child in self.children:
            if not isinstance(child, YaReally):
                continue
            c += indent(child.to_c(), 1)
        c += "\n}"

        # 'else-if' bodies:
        c += "\n".join(
            [child.to_c() for child in self.children if isinstance(child, Maybe)]
        )

        # 'else' body:
        c += "\n".join(
            [child.to_c() for child in self.children if isinstance(child, NoWai)]
            [:1]  # max 1 else-body
        )
        return c


class ExpressionChild(Element):

    def diagnostics(self):
        return [] if isinstance(self.parent, Expression) else [
            Diagnostic(
                Severity.ERROR,
                self.code_range,
                "{} element found outside of expression element".format(self.tagname)
            )
        ]


class YaReally(ExpressionChild):

    def to_c(self):
        return self.children_to_c()


class Maybe(ExpressionChild):

    def __init__(self):
        super().__init__()
        self.x = None

    def init(self):
        self.x = self.attributes.get("x", "").get("val")

    def diagnostics(self):
        d = super().diagnostics()
        if not self.x:
            d.append(Diagnostic(
                Severity.ERROR,
                self.code_range,
                "Maybe element found without x-attribute"
            ))
        return d

    def to_c(self):
        return " else if ({})".format(self.x) + " {\n" + (

            indent(self.children_to_c(), 1)

        ) + "}"


class NoWai(ExpressionChild):

    def to_c(self):
        return " else {\n" + indent(self.children_to_c(), 1) + "}\n"
