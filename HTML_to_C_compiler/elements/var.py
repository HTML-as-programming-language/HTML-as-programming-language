from elements.element import Element
from utils import hyphenated_to_camel_case


class Var(Element):
    """"
    HTML:

    <var b=6/>
    <var aString="hello"/>
    <var aChar='b'/>

    C:
    int b = 6;
    String aString = "hello";
    char aChar = 'b';
    """

    def to_c(self):

        var_name = None
        attr = None
        for key in self.attributes:
            if key == "type":
                continue
            var_name = hyphenated_to_camel_case(key)
            attr = self.attributes[key]

        if not var_name:
            raise Exception(
                "No variable name defined at line {}".format(self.line)
            )

        val = attr["val"]

        typee = self.attributes.get("type", {}).get("val")
        if typee is None:                         # user did not provide type like <var x=y type="int"/>
            typee = attr["type"] or "unknown"     # Guessed type

        if typee == "unknown":
            raise Exception(
                "Unknown variable type at line {}"
                "\nPlease provide a type in the type attribute like <var x=y type='int'/>"
                    .format(self.line)
            )

        if typee == "String":
            val = '"{}"'.format(val)
        elif typee == "char":
            val = "'{}'".format(val)

        return "{} {} = {};\n".format(typee, var_name, val)
