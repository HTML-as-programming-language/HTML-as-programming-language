from elements.element import Element
from utils import includeFile


class Doctype(Element):
    """"
    Een variabel om te bepalen wat voor platform de code voor bedoeld is (e.g: arduino) html is pc
    HTML: <!DOCTYPE html>
    """

    def to_c(self):
        if self.attributes.get("text", "") == "<!DOCTYPE arduino>":
            return includeFile("libraries/arduinoLib.c") + "\n"
        else:
            return self.attributes.get("text", "") + "\n" #TODO niet dit
