from htmlc.elements.element import Element


class FunctionCall(Element):
    """"
    HTML:
    <funcname>
        <param ... />
    </funcname>

    C: funcname(param1, param2, etc..)
    """

    def to_c(self, mapped_c):

        params = []
        # get params:
        for el in self.children:
            if el.tagname == "param":
                params.append(el.data.strip())

        line = "{}({})".format(  # for example: multiply(4, 5)
            self.tagname,
            ", ".join([param for param in params]))

        # if this functioncall is not a child of a functioncall, add a semicolon
        if not (isinstance(self.parent, FunctionCall)):
            line += ";"

        mapped_c.add(line + "\n", self)

