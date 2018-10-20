import re

from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element


class Have(Element):

    class What:
        PILE_THING = 1

    def __init__(self):
        super().__init__()
        self.is_value = True
        self.have_what: Have.What = None
        self.have_what_nr = 0
        self.have_of_what = None

    def init(self):
        attr_keys = self.attributes.keys()
        for ak in attr_keys:
            if re.fullmatch("nr\d+", ak):
                self.have_what = Have.What.PILE_THING
                self.have_what_nr = ak[2:]

            elif ak == "nr":
                nr = self.attributes[ak].get("val")
                if isinstance(nr, int) or (isinstance(nr, str) and len(nr) > 0):
                    self.have_what = Have.What.PILE_THING
                    self.have_what_nr = nr

            elif ak == "of":
                self.have_of_what = self.attributes[ak].get("val") or self.data.strip()
        if not self.have_what:
            self.is_value = False

    def diagnostics(self):
        d = []
        if not self.have_what:
            d.append(Diagnostic(
                Severity.WARNING, self.code_range,
                "WHAT DO YOU WANT?!!??!"
            ))
        elif self.have_what is Have.What.PILE_THING and not self.have_of_what:
            d.append(Diagnostic(
                Severity.ERROR, self.code_range,
                f"From which pile do you want number {self.have_what_nr}?\n"
                f"eg: <have nr{self.have_what_nr} of>myPile</have>"
            ))

        if not self.parent.is_value_wrapper:
            d.append(Diagnostic(
                Severity.WARNING, self.code_range,
                "Having this is useless"
            ))
        return d

    def to_c(self, mapped_c):
        if not self.parent.is_value_wrapper or not self.have_what:
            return

        if self.have_what is Have.What.PILE_THING:
            mapped_c.add(f"{self.have_of_what}[{self.have_what_nr}]", self)

