from elements.element import Element
from utils import remove_indentation


class C(Element):
    """"
    HTML: <c>c-code</c>
    C: ..........
    """
    def to_c(self):
        return remove_indentation(self.data + "\n")
