from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.element import Element
from htmlc.elements.pile_elements.pile_action import PileAction


class Upgrade(PileAction):

    def __init__(self):
        super().__init__()
        self.is_value_wrapper = True

    def of_unspecified_err_msg(self):
        return (
            f"Of what pile do you want to upgrade number {self.nr}?\n"
            f"eg: <upgrade nr{self.nr} of=\"myPile\" to>100</have>"
        )

    def diagnostics(self):
        return (
            super().diagnostics()
            if self.to or not self.of or not self.nr
            else
            [*super().diagnostics(), Diagnostic(
                Severity.ERROR, self.code_range,
                f"Pls say what the thing should be upgraded to.\n"
                "eg: <upgrade to>upgradeToThis</upgrade"
            )]
        )

    def to_c(self, mapped_c):
        mapped_c.add(f"{self.of}[{self.nr}] = ", self)
        if isinstance(self.to, Element):
            self.to.to_c(mapped_c)
        else:
            mapped_c.add(f"{self.to}", self)
        mapped_c.add(";\n", self)
