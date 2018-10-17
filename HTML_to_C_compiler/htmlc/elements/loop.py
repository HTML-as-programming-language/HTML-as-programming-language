from htmlc.elements.element import Element


class Loop(Element):
    """"
    HTML:
    <loop to=5>                 from=0 and step=1 are defaults
    <loop from=2 to=5 step=2>

    C:
    for(int i=0; i<=5; i+=1) { ... }
    """

    def to_c(self, mapped_c):

        # var_from = 0 + self.attributes["from"]
        from_type = self.attributes.get("from", {}).get("type", "int")
        from_value = self.attributes.get("from", {}).get("val", 0)   # start from 0 if noting is given in 

        to_type = self.attributes.get("to", {}).get("type", "int")
        to_value = self.attributes.get("to", {}).get("val", -1)      # infinite loop if no "to" given in

        step_type = self.attributes.get("step", {}).get("type", "int")
        step_value = self.attributes.get("step", {}).get("val", 1)   # the default is i++

        mapped_c.add(
            f"\nfor({from_type} i={from_value}; i<{to_value}; i+={step_value})" + " {\n",
            self
        )
        mapped_c.indent(1)
        self.children_to_c(mapped_c)
        mapped_c.indent(-1)
        mapped_c.add("\n}\n\n", self)