from htmlc.elements.element import Element
from htmlc.utils import hyphenated_to_camel_case


class Truth(Element):
    """"
    HTML: <truth>x</truth>
    C: bool x = true;
    """

    def to_c(self):
        if not self.data:
            raise Exception(
                "Please provide bool name like: <truth>i-am-an-idiot</truth> on line {}"
                    .format(self.line)
            )

        return "bool {} = true;\n".format(
            hyphenated_to_camel_case(
                "".join(self.data.split())
            )
        )


class Lie(Element):
    """"
    HTML: <lie>y</lie>
    C: bool y = false;
    """

    def to_c(self):
        if not self.data:
            raise Exception(
                "Please provide bool name like: <truth>i-am-an-idiot</truth> on line {}"
                    .format(self.line)
            )

        return "bool {} = false;\n".format(
            hyphenated_to_camel_case(
                "".join(self.data.split())
            )
        )
