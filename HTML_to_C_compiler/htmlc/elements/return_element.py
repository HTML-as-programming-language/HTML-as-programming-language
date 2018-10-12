from htmlc.elements.element import Element


class Return(Element):
    """"
    HTML: <return>5</return>
    C: return 5;
    """

    def to_c(self):
        return "return {};\n".format(self.data.strip())
