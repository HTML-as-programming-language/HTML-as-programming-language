from htmlc.elements.element import Element


class Rise(Element):

    def to_c(self, mapped_c):
        if not len(self.attributes):
            return
        name = list(self.attributes.keys())[0]

        max = self.attributes.get("max", {}).get("val")

        if max:
            mapped_c.add(
                f"{name} = ({name} >= {max}) ? 0 : ({name} + 1);\n", self
            )
        else:
            mapped_c.add(f"{name}++;\n", self)
