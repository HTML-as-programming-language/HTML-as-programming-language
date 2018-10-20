
from htmlc.elements.pile_elements.pile_action import PileAction


class Have(PileAction):

    def __init__(self):
        super().__init__()
        self.is_value = True

    def of_unspecified_err_msg(self):
        return (
            f"From which pile do you want number {self.nr}?\n"
            f"eg: <have nr{self.nr} of>myPile</have>"
        )

    def to_c(self, mapped_c):
        if not self.parent.is_value_wrapper:
            return

        mapped_c.add(f"{self.of}[{self.nr}]", self)
