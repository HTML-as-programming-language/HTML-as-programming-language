from htmlc.elements.element import Element


class Infinity(Element):

    def to_c(self, mapped_c):
        mapped_c.add("while (cake) {\n", self)
        mapped_c.indent(1)
        self.children_to_c(mapped_c)
        mapped_c.indent(-1)
        mapped_c.add("}\n", self)
