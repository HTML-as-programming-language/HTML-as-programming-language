from elements.element import Element
from utils import hyphenated_to_camel_case

class Include(Element):
    """
    HTML:
    <include> package.h </include>
    C/ino:
    #include <package.h>

    TODO: add the functionality to include .html files to the html code
    """

    def to_c(self):
        return "#include <{}>\n".format(hyphenated_to_camel_case("".join(self.data.split())))
