from htmlc.elements.element import Element


class Link(Element):
    """
    HTML:
    <link type="text/html" href="./include-this-file.html"/>
    """

    def to_c(self):
        return self.children_to_c()


class Script(Link):
    """
    HTML:
    <script type="text/html" src="./include-this-file.html"/>
    """
    pass