
class Element:

    def __init__(self):
        self.data = None
        self.attributes = {}
        self.children = []
        self.parent = None
        self.tagname = ""
        self.line = -1

    def to_c(self):
        return ""
