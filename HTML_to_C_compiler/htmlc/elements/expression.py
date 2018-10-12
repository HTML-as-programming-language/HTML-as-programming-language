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

    def to_c(self):

        x = self.attributes.get("x", "").get("val")
        if not x:
            raise Exception("Expression element found without x-attribute on line {}".format(self.line))
        # 'if' body:
        c = "if ({})".format(x) + " {\n"
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

    def check(self):
        if not isinstance(self.parent, Expression):
            raise Exception(
                "{} element found outside of expression element on line {}".format(self.tagname, self.line)
            )


class YaReally(ExpressionChild):

    def to_c(self):
        self.check()
        return self.children_to_c()


class Maybe(ExpressionChild):

    def to_c(self):
        self.check()
        x = self.attributes.get("x", "").get("val")
        if not x:
            raise Exception("Maybe element found without x-attribute on line {}".format(self.line))
        return " else if ({})".format(x) + " {\n" + (

            indent(self.children_to_c(), 1)

        ) + "}"


class NoWai(ExpressionChild):

    def to_c(self):
        self.check()
        return " else {\n" + indent(self.children_to_c(), 1) + "}\n"
