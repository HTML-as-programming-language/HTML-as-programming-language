from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element


class DigitalWrite(Element):

    def __init__(self):
        super().__init__()
        self.val = None
        self.name = None
        self.is_value_wrapper = True
        self.require_htmlc_includes = [
            "avr/digital.c"
        ]

    def init(self):
        if not len(self.attributes):
            return

        self.name, attr = list(self.attributes.items())[0]
        self.val = attr.get("val") or self.get_inner_value()

    def diagnostics(self):
        return [] if self.name else [Diagnostic(
            Severity.ERROR, self.code_range,
            "Use like: <digital-write myLed>cake</digital-write>"
        )]

    def to_c(self, mapped_c):
        mapped_c.add(
            f"\n// write {self.val} to {self.name}:\n"
            f"digital_write(&__{self.name}_PORT__, __{self.name}_BIT_NR__, ",
            self
        )
        if isinstance(self.val, Element):
            self.val.to_c(mapped_c)
        else:
            mapped_c.add(f"{self.val}", self)
        mapped_c.add(");\n", self)
