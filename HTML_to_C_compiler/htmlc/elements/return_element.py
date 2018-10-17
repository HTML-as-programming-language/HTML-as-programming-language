from htmlc.elements.element import Element


class Return(Element):
    """"
    HTML: <return>5</return>
    C: return 5;
    """

    def to_c(self, mapped_c):
        mapped_c.add(f"return {self.data.strip()};\n", self)
