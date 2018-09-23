from elements.element import Element
from utils import hyphenated_to_camel_case, indent


class Loop(Element):
    """"
    HTML:
    <loop to=5>                 from=0 and step=1 are defaults
    <loop from=2 to=5 step=2>

    C:
    for(int i=0; i<=5; i+=1) { ... }
    """

    def to_c(self):

        # var_from = 0 + self.attributes["from"]
        from_type = self.attributes.get("from", {}).get("type", "int")
        from_value = self.attributes.get("from", {}).get("val", 0)

        to_type = self.attributes.get("to", {}).get("type", "int")
        to_value = self.attributes.get("to", {}).get("val", 0)

        step_type = self.attributes.get("step", {}).get("type", "int")
        step_value = self.attributes.get("step", {}).get("val", 1)


        c = "\n\nfor({} i={}; i<{}; i+={})".format(
            from_type, from_value,
            to_value,
            step_value
        ) + " {\n"

        for el in self.children:
            if el.tagname == "param":
                continue
            el_c = el.to_c()
            if el_c:
                c += indent(el_c, 1)

        c += "}\n"
        return c