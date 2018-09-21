from elements.assembly import Assembly
from elements.assign import Assign
from elements.boolean_elements import Truth, Lie
from elements.c import C
from elements.comment import Comment
from elements.function import Def, Param
from elements.function_call import FunctionCall
from elements.return_element import Return
from elements.var import Var
from html_parser.parser import HTMLParser
from utils import camel_case_to_hyphenated


class Compiler(HTMLParser):

    def __init__(self):
        self.current_element = None
        self.elements = []
        self.element_classes = [
            Var,        # <var a=5/>
            Truth,      # <truth>x</truth>
            Lie,
            Assign,
            C,
            Assembly,
            Def,        # <def functionname></def>
            Param,
            Return,
            Comment     # <!-- this is a comment --> OR <comment text="this is a comment"/>
        ]

    def handle_starttag(self, tagname, attrs, line):
        # print("start:", tagname)
        new_element = self.new_element_by_tagname(tagname)
        new_element.tagname = tagname
        new_element.attributes = attrs
        new_element.line = line
        if self.current_element:
            self.current_element.children.append(new_element)
            new_element.parent = self.current_element
        else:
            self.elements.append(new_element)

        self.current_element = new_element

    def handle_data(self, data, line):
        # print("data:", data)
        if self.current_element:
            self.current_element.data = data

    def handle_closingtag(self, tagname, line):
        # print("closing tag:", tagname)
        if self.current_element and tagname == self.current_element.tagname:
            self.current_element = self.current_element.parent
        elif self.current_element:
            raise Exception(
                "Expected closing tag: </{}>\nGot: </{}> on line {}"
                    .format(self.current_element.tagname, tagname, line)
            )
        else:
            raise Exception("Unexpected closing tag </{}> on line {}".format(tagname, line))

    def handle_comment(self, comment_text, line):
        # print("comment on line {}:".format(line), comment_text)
        self.handle_starttag("comment", {"text": comment_text}, line)
        self.handle_closingtag("comment", line)

    def new_element_by_tagname(self, tagname):
        for el in self.element_classes:
            if camel_case_to_hyphenated(el.__name__) == tagname:
                return el()
        # no element found so assume its a function call:
        return FunctionCall()

    def finish_parsing(self):
        if self.current_element:
            raise Exception(
                "Unclosed element <{}> on line {}\nDid you mean <{} ...attributes... /> ?".format(
                    self.current_element.tagname,
                    self.current_element.line,
                    self.current_element.tagname
                )
            )

    def to_c(self):

        c = ""
        for el in self.elements:
            el_c = el.to_c()
            if el_c:
                c += el.to_c()

        return c


compiler = Compiler()
compiler.feed("../working-code.html")
c = compiler.to_c()
print(c)

file = open("../working-code.c", "w")
file.write(c)
file.close()

while 1:
    pass