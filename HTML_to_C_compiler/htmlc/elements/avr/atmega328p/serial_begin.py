from htmlc.elements.element import Element


class SerialBegin(Element):

    def __init__(self):
        super().__init__()
        self.require_htmlc_includes = ["avr/atmega328p/serial.c"]

    def to_c(self, mapped_c):
        baud = self.get_inner_value() or 9600
        f_cpu = self.attributes.get("clock-freq", {}).get("val")
        if not f_cpu:
            f_cpu = 16000000
        elif isinstance(f_cpu, str) and f_cpu.endswith("MHz"):
            f_cpu = f_cpu.replace("MHz", "000000")
        mapped_c.add(f"serial_begin(", self)
        if isinstance(baud, Element):
            baud.to_c(mapped_c)
        else:
            mapped_c.add(f"{baud}", self)
        mapped_c.add(f", {f_cpu});\n", self)
