from htmlc.elements.element import Element


class SerialReceive(Element):

    def __init__(self):
        super().__init__()
        self.is_value = True

    def to_c(self, mapped_c):
        if self.parent and self.parent.is_value_wrapper:
            mapped_c.add("serial_receive()", self)

