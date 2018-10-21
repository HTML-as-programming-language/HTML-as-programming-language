from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element


class PinMode(Element):
    OUTPUT = 1
    INPUT = 2

    def __init__(self):
        super().__init__()
        self.mode = None
        self.name = None
        self.require_htmlc_includes = [
            "avr/digital.c"
        ]

    def init(self):
        for key, attr in self.attributes.items():
            val = attr.get("val")
            if not (val == "input" or val == "output"):
                continue
            self.name = key
            self.mode = PinMode.INPUT if val == "input" else PinMode.OUTPUT

    def diagnostics(self):
        return [] if self.name else [
            Diagnostic(
                Severity.ERROR, self.code_range,
                'Use like: <pin-mode myLed="output"/> (or input)\n'
                'Where "myLed" is the name of the pin that you must have defined with a <pin> tag'
            )
        ]

    def to_c(self, mapped_c):
        mapped_c.add(
            f"\n// set {self.name} as {'output' if self.mode == PinMode.OUTPUT else 'input'}:\n"
            f"digital_write(&__{self.name}_DDR__, __{self.name}_BIT_NR__, "
            +
            ("cake" if self.mode == PinMode.OUTPUT else "lie")
            +
            ");\n",
            self
        )
