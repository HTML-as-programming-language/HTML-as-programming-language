from htmlc.elements.element import Element


class SerialTransmit(Element):

    def __init__(self):
        super().__init__()
        self.is_value_wrapper = True

    def to_c(self, mapped_c):
        val = self.get_inner_value()
        if not val:
            return
        mapped_c.add("serial_transmit(", self)
        if isinstance(val, Element):
            val.to_c(mapped_c)
        else:
            mapped_c.add(f"{val}", self)
        mapped_c.add(");\n", self)


class SerialPrint(Element):

    def __init__(self):
        super().__init__()
        self.is_value_wrapper = True

    def to_c(self, mapped_c):
        val = self.get_inner_value()
        if not val:
            return
        mapped_c.add("serial_print(", self)
        if isinstance(val, Element):
            val.to_c(mapped_c)
        else:
            mapped_c.add(f"{val}", self)
        mapped_c.add(");\n", self)
