from htmlc.elements.element import Element
from htmlc.utils import remove_indentation


class C(Element):
    """"
    HTML: <c>c-code</c>
    C: ..........
    """
    def to_c(self, mapped_c):
        mapped_c.add(self.data + "\n\n", self)
