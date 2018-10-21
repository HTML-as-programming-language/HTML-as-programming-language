from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element


class DigitalRead(Element):

    def __init__(self):
        super().__init__()
        self.is_value = True
        self.require_htmlc_includes = [
            "avr/digital.c"
        ]
        self.name = None

    def init(self):
        if not len(self.attributes):
            return
        self.name = list(self.attributes.keys())[0]

    def diagnostics(self):
        return [] if self.name else [Diagnostic(
            Severity.ERROR, self.code_range,
            "Pls give a Pin-name to read.\n"
            "eg: <digital-read myButton/>\n"
            "where myButton is defined at the top of the file like:\n"
            "<pin myButton=\"D0\"/>"
        )]

    def to_c(self, mapped_c):
        if self.parent and self.parent.is_value_wrapper:
            mapped_c.add(
                f"digital_read(&__{self.name}_PIN__, __{self.name}_BIT_NR__)",
                self
            )
