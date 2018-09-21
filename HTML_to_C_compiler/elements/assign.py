from elements.element import Element


class Assign(Element):
    """"
    HTML: <assign a>5</assign>
    C: a = 5
    """

    def to_c(self):

        var_name = None
        for key in self.attributes:
            var_name = key

        if var_name is None:
            raise Exception(
                "No variable name given in assign tag at line {}".format(self.line)
            )

        if self.data is None:
            raise Exception(
                "Cannot assign nothing to '{}' on line {}".format(var_name, self.line)
            )

        return "{} = {};\n".format(var_name, self.data.strip())
