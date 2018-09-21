from elements.element import Element


class FunctionCall(Element):
    """"
    HTML:
    <funcname>
        <param ... />
    </funcname>

    C: funcname(param1, param2, etc..)
    """

    def to_c(self):

        params = []
        for el in self.children:
            if el.tagname == "param":
                params.append(el.data.strip())

        return "{}({})\n".format(
            self.tagname,
            ", ".join([param for param in params])
        )
