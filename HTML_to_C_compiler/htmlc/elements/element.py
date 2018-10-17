
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
