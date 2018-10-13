from htmlc.code_range import CodeRange
from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.assembly import Assembly
from htmlc.elements.assign import Assign
from htmlc.elements.boolean_elements import Truth, Lie
from htmlc.elements.c import C
from htmlc.elements.comment import Comment
from htmlc.elements.doctype import Doctype
from htmlc.elements.expression import Expression, YaReally, Maybe, NoWai
from htmlc.elements.function import Def, Param
from htmlc.elements.function_call import FunctionCall
from htmlc.elements.link import Link, Script
from htmlc.elements.loop import Loop
from htmlc.elements.return_element import Return
from htmlc.elements.var import Var
from htmlc.html_parser import HTMLParser
from htmlc.utils import camel_case_to_hyphenated


class Lexer(HTMLParser.Handler):
    """
    The Lexer handles data that is parsed by a HTMLParser
    with this data the lexer will construct an element tree.

    The element tree can only contain elements listed in self.element_classes.

    Every element must have a to_c() method.
    It should return the corresponding C code. (or None if it has no corresponding code)

    For example:
    (<var a=5/>).to_c()
    should return:
    "int a = 5;"
    """

    def __init__(self, dir, filename):
        self.dir = dir
        self.filename = filename
        self.current_element = None
        self.elements = []
        self.element_classes = [
            Var,        # <var a=5/>
            Truth,      # <truth>x</truth>
            Lie,
            Loop,
            Assign,
            C,
            Assembly,
            Def,        # <def functionname></def>
            Param,
            Return,
            Comment,    # <!-- this is a comment --> OR <comment text="this is a comment"/>
            Link,       # <link type="text/html" href="./include-this-file.html"/>
            Script,      # <script type="text/html" src="./include-this-file.html"/>
            Doctype,
            Expression, YaReally, Maybe, NoWai      # if/else if/else functionality
        ]
        self.diagnostics = []

    def handle_starttag(self, tagname, attrs, line, char, endchar):
        """
        Create a new element and put it in the element tree
        All future elements will be a child of this element UNTIL handle_closingtag() is called
        """
        new_element = self.new_element_by_tagname(tagname)
        new_element.tagname = tagname
        new_element.attributes = attrs
        new_element.code_range = CodeRange(self.dir, self.filename, line, char, line, endchar)

        if self.current_element:
            self.current_element.children.append(new_element)
            new_element.parent = self.current_element
        else:
            self.elements.append(new_element)

        self.current_element = new_element

    def handle_data(self, data, line):
        if self.current_element:
            if self.current_element.data:
                self.current_element.data += data
            else:
                self.current_element.data = data

    def handle_closingtag(self, tagname, line, char, endchar):
        """
        End of element found.
        self.current_element = self.current_element.parent
        """
        if self.current_element and tagname == self.current_element.tagname:
            self.current_element.code_range.endline = line
            self.current_element.code_range.endchar = endchar
            self.current_element = self.current_element.parent
        elif self.current_element:
            self.diagnostics.append(Diagnostic(
                Severity.ERROR,
                CodeRange(self.dir, self.filename, line, char, line, endchar),
                f"Expected closing tag: </{self.current_element.tagname}>\nGot: </{tagname}>"
            ))
        else:
            self.diagnostics.append(Diagnostic(
                Severity.ERROR,
                CodeRange(self.dir, self.filename, line, char, line, endchar),
                f"Unexpected closing tag </{tagname}>"
            ))

    def handle_comment(self, comment_text, line, char, endchar):
        self.handle_starttag("comment", {"text": comment_text}, line, char, endchar)
        self.handle_closingtag("comment", line, char, endchar)

    def handle_doctype(self, doctype):
        self.handle_starttag("doctype", {"text": doctype}, 0, 0, 0)
        self.handle_closingtag("doctype", 0, 0, len(doctype))

    def new_element_by_tagname(self, tagname):
        """
        Creates an new element based on the tagname.
        tagname 'var' will return Var()
        tagname 'def' will return Def()
        tagname 'this-is-a-function-call' is not a known element so it will return FunctionCall()
        """
        for el in self.element_classes:
            if camel_case_to_hyphenated(el.__name__) == tagname:
                return el()
        # no element found so assume its a function call:
        return FunctionCall()

    def finish_parsing(self):
        """
        Called when reading the HTML file is done.

        If there is still an open element (self.current_element != None)
        it means that there's an unclosed element somewhere in the file
        """
        if self.current_element:
            self.diagnostics.append(Diagnostic(
                Severity.ERROR,
                self.current_element.code_range,
                "Unclosed element <{}>\nDid you mean <{} ...attributes... /> ?".format(
                    self.current_element.tagname,
                    self.current_element.tagname
                )
            ))
