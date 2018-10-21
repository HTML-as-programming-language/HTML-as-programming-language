from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element


class Link(Element):
    """
    HTML:
    <link type="text/html" href="./include-this-file.html"/>
    """

    def to_c(self, mapped_c):
        self.children_to_c(mapped_c)

    def diagnostics(self):
        if not self.src():
            return[Diagnostic(
                Severity.ERROR,
                self.code_range,
                f"Found {self.tagname} element without {self.src_attr_name()} attribute"
            )]
        return []

    def src(self):
        return self.attributes.get(self.src_attr_name(), {}).get("val")

    def src_attr_name(self):
        return "src" if self.tagname == "script" else "href"

    def link_type(self):
        return self.attributes.get("type", {}).get("val")


class Script(Link):
    """
    HTML:
    <script type="text/html" src="./include-this-file.html"/>
    """
    pass