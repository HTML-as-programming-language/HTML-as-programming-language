import re

from htmlc.diagnostics import Severity, Diagnostic
from htmlc.elements.element import Element


class PileAction(Element):

    def __init__(self):
        super().__init__()
        self.nr = 0
        self.of = None
        self.to = None

    def init(self):
        attr_keys = self.attributes.keys()
        for ak in attr_keys:
            if re.fullmatch("nr\d+", ak):
                self.nr = ak[2:]

            elif ak == "nr":
                self.nr = self.attributes[ak].get("val") or 0

            elif ak == "of":
                self.of = self.attributes[ak].get("val") or self.data.strip()

            elif ak == "to":
                self.to = self.attributes[ak].get("val") or self.get_inner_value()

    def diagnostics(self):
        d = []
        if not self.nr:
            d.append(Diagnostic(
                Severity.ERROR, self.code_range,
                f"Specify the number like: <{self.tagname} nr3 ..> OR <{self.tagname} nr=i ..>"
            ))
        elif not self.of:
            d.append(Diagnostic(
                Severity.ERROR, self.code_range,
                self.of_unspecified_err_msg()
            ))

        if not self.parent.is_value_wrapper and self.is_value:
            d.append(Diagnostic(
                Severity.WARNING, self.code_range,
                f"Result of <{self.tagname}> is ignored"
            ))
        return d

    def of_unspecified_err_msg(self):
        pass
