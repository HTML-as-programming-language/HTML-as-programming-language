from htmlc.elements.element import Element


class Rise(Element):

    def __init__(self):
        super().__init__()
        self.operator = "+"

    def to_c(self, mapped_c):
        if not len(self.attributes):
            return
        name = list(self.attributes.keys())[0]

        max = self.attributes.get("max", {}).get("val")
        min = self.attributes.get("min", {}).get("val")
        step = self.attributes.get("step", {}).get("val") or 1
        reset = self.attributes.get("reset", {}).get("val") or 0

        mapped_c.add(
            f"{name} = ", self
        )
        if max:
            mapped_c.add(
                f"{name} >= {max} ? {reset} : ", self
            )
        mapped_c.add("(", self)
        if min:
            mapped_c.add(
                f"{name} <= {min} ? {reset} : ", self
            )
        mapped_c.add(f"{name} {self.operator} {step});\n", self)


class Fall(Rise):

    def __init__(self):
        super().__init__()
        self.operator = "-"
