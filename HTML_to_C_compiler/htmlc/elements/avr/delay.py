from htmlc.elements.element import Element


class Delay(Element):

    def __init__(self):
        super().__init__()
        self.require_includes = ["util/delay.h"]

    def to_c(self, mapped_c):
        mapped_c.add("_delay_ms(", self)
        val = self.get_inner_value()
        if isinstance(val, Element):
            val.to_c(mapped_c)
        else:
            if not val:
                val = 0
            elif isinstance(val, str):
                if val.endswith("ms"):
                    val = val[:-2]
                elif val.endswith("s") and val[:-1].isdigit():
                    val = int(val[:-1]) * 1000

            mapped_c.add(f"{val}", self)
        mapped_c.add(");\n", self)
