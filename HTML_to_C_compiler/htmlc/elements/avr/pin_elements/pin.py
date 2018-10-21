import re

from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element


class Pin(Element):

    def __init__(self):
        super().__init__()
        self.name = None
        self.mode = None
        self.char = None
        self.bit_nr = None
        self.require_includes = ["avr/io.h"]

    def init(self):
        for key, attr in self.attributes.items():
            val = attr.get("val")
            if not isinstance(val, str) or not re.fullmatch("[A-Z]\d+", val):
                continue
            self.name = key
            self.char = val[:1]
            self.bit_nr = int(val[1:])
            break

    def diagnostics(self):
        d = []
        if not self.name:
            d.append(
                Diagnostic(
                    Severity.ERROR, self.code_range,
                    'Define a pin like: <pin myLed="D3"/>\n'
                    "Where myLed is the pin-name and D3 means the third bit of PORTD"
                )
            )
        return d

    def to_c(self, mapped_c):
        mapped_c.add(
            f"// pin {self.name}:\n"
            f"#define __{self.name}_BIT_NR__ {self.bit_nr}\n"
            f"#define __{self.name}_PORT__ PORT{self.char}\n"
            f"#define __{self.name}_DDR__ DDR{self.char}\n"
            f"#define __{self.name}_PIN__ PIN{self.char}\n",
            self
        )

