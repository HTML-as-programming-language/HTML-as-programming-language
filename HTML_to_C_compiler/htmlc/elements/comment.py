from htmlc.elements.element import Element


class Comment(Element):
    """"
    HTML: <!-- this is a comment -->
    C: // this is a comment
    """

    def to_c(self):
        return "//" + self.attributes.get("text", "").replace("\n", "\n// ") + "\n"
