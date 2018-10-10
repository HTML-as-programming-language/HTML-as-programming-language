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
        iftrues = ""
        elseifs = []
        iffalse = ""

        for item in self.children:
            c = item.to_c()
            if (c == "no-wai();\n"):
                for child in item.children: #adds items to the else field of the if statement
                    iffalse += (child.to_c())
                continue
            if (c == "maybe();\n"):
                subelseif = "" #create empty string
                for child in item.children: #adds items to the else if field of the if statement
                    subelseif += (child.to_c()) #adds else if field to elseifs
                elseifs.append(subelseif)
                continue

            if (c == "ya-really();\n"):#if not part of else or else if field, add to if statement
                for child in item.children:  # adds items to the if state of the if statement
                    iftrues += (child.to_c())
                continue

        lineToReturn = ("if (" + self.attributes.get("text", "") + ") {\n") + iftrues + " }\n" #build the if statement
        for item in elseifs: #write else if statement one by one
            lineToReturn += "else if() {\n"
            lineToReturn += item
            lineToReturn += "}\n"
        if (iffalse != ""): #write the else statement
            lineToReturn += "else {\n" + iffalse + "}\n"

        return(lineToReturn)