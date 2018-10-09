from elements.element import Element


class Expression(Element):
    """"
    HTML: <expression x="a > 50">
    <ya-really>
        <!-- if-code here -->
    </ya-really>

    <maybe x="a < 10">
        <!-- else-if code here -->
    </maybe>

    <no-wai>
        <!-- else code here -->
    </no-wai>
    </expression>

    C: if (a > 50){
    //code goes here
    }
    else if (a < 10) {
    //else-if code here
    }
    else {
    //else code here
    }
    """

    def to_c(self):
        print (str(self.attributes))
        x = ""
        for item in self.children:
            x += (item.to_c() + "\n")

        return("if (" + self.attributes.get("text", "") + ") {\n" +
               x + "}" + "\n")