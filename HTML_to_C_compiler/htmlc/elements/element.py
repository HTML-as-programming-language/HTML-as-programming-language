
class Element:

    def __init__(self):
        self.data = None
        self.attributes = {}
        self.children = []
        self.parent = None
        self.tagname = ""
        self.code_range = None

    def init(self):
        pass

    def diagnostics(self):
        """
        Should return a list of Diagnostics
        """
        return []

    def to_c(self):
        return ""

    def children_to_c(self):
        c = ""
        for el in self.children:
            el_c = el.to_c()
            if el_c:
                c += el_c

        return c
