
class Element:

    def __init__(self):
        self.data = None
        self.attributes = {}
        self.children = []
        self.parent = None
        self.tagname = ""
        self.line = -1
        self.dir = "./"
        self.filename = ""

    def to_c(self):
        return ""

    def children_to_c(self):
        c = ""
        for el in self.children:
            el_c = el.to_c()
            if el_c:
                c += el_c

        return c
