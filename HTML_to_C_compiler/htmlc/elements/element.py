from typing import List

from htmlc.code_range import CodeRange


class Element:

    def __init__(self):
        self.data = None
        self.attributes = {}
        self.children: List[Element] = []
        self.parent: Element = None
        self.tagname = ""
        self.code_range: CodeRange = None
        self.is_value_wrapper = False       # true if element can wrap values,
                                            # eg: <assign a><have enormity of>myPile</have</assign>
        self.is_value = False               # true if element can be wrapped

    def init(self):
        pass

    def init_children(self):
        for child in self.children:
            child.init()
            child.init_children()

    def diagnostics(self):
        """
        Should return a list of Diagnostics
        """
        return []

    def to_c(self, mapped_c):
        pass

    def children_to_c(self, mapped_c):
        for el in self.children:
            el.to_c(mapped_c)

    def get_inner_value(self):
        for el in self.children:
            if el.is_value:
                return el

        return self.data.strip()
