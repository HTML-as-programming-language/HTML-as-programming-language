from elements.element import Element


class Doctype(Element):
    """"
    Een variabel om te bepalen wat voor platform de code voor bedoeld is (e.g: arduino) html is pc
    HTML: <!DOCTYPE html>
    """

    def to_c(self):
        return self.attributes.get("text", "") + "\n" #TODO niet dit
