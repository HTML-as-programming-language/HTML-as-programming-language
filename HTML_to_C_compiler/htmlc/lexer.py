from htmlc.elements.avr.atmega328p.serial_begin import SerialBegin
from htmlc.elements.avr.atmega328p.serial_receive import SerialReceive
from htmlc.elements.avr.atmega328p.serial_transmit import SerialTransmit, \
    SerialPrint
from htmlc.elements.avr.pin_elements.digital_read import DigitalRead
from htmlc.elements.avr.pin_elements.digital_write import DigitalWrite
from htmlc.elements.avr.pin_elements.pin import Pin
from htmlc.elements.avr.pin_elements.pin_mode import PinMode
from htmlc.elements.infinity import Infinity
from htmlc.elements.pile_elements.have import Have

from htmlc.code_range import CodeRange
from htmlc.diagnostics import Diagnostic, Severity
from htmlc.elements.assembly import Assembly
from htmlc.elements.assign import *
from htmlc.elements.boolean_elements import Cake, Lie
from htmlc.elements.c import C
from htmlc.elements.comment import Comment
from htmlc.elements.expression import Expression, YaReally, Maybe, NoWai
from htmlc.elements.function import Def, Param
from htmlc.elements.function_call import FunctionCall
from htmlc.elements.link import Link, Script
from htmlc.elements.loop import Loop
from htmlc.elements.pile_elements.pile import Pile, Thing
from htmlc.elements.pile_elements.upgrade import Upgrade
from htmlc.elements.return_element import Return
from htmlc.elements.rise_and_fall import Fall, Rise
from htmlc.elements.var_and_const import Var, Const
from htmlc.elements.what_is import WhatIs
from htmlc.html_parser import HTMLParser
from htmlc.utils import camel_case_to_hyphenated


class Lexer(HTMLParser.Handler):
    """
    The Lexer handles data that is parsed by a HTMLParser
    with this data the lexer will construct an element tree.

    The element tree can only contain elements listed in self.element_classes.
    """

    def __init__(self, dir, filename):
        self.dir = dir
        self.filename = filename
        self.doctype = None
        self.current_element = None
        self.elements = []
        self.element_classes = [
            Var, Const,  # <var a=5/>
            Assign, Add, Minus, AndBits, OrBits, XorBits, Multiply, Divide,
            Modulo,
            Cake,  # <truth>x</truth>
            Lie,
            Have,
            Upgrade,
            Loop,
            Infinity,
            C,
            Assembly,
            Def,  # <def functionname></def>
            Param,
            Return,
            Comment,  # <!-- this is a comment -->
            Link,  # <link type="text/html" href="./include-this-file.html"/>
            Script,  # <script type="text/html" src="./include.html"/>
            Expression, YaReally, Maybe, NoWai,
            # if/else if/else functionality
            Pile, Thing,  # Arrays
            WhatIs,
            Rise, Fall  # ++ / --

            # AVR elements are added when handle_doctype("avr/....") is called
        ]
        self.diagnostics = []

    def handle_starttag(self, tagname, attrs, line, char, endchar):
        """
        Create a new element and put it in the element tree
        All future elements will be a child of this element
        UNTIL handle_closingtag() is called
        """
        new_element = self.new_element_by_tagname(tagname)
        new_element.tagname = tagname
        new_element.attributes = attrs
        new_element.code_range = CodeRange(self.dir, self.filename, line, char,
                                           line, endchar)

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
                f"Expected closing tag: </{self.current_element.tagname}>\n"
                f"Got: </{tagname}>"
            ))
        else:
            self.diagnostics.append(Diagnostic(
                Severity.ERROR,
                CodeRange(self.dir, self.filename, line, char, line, endchar),
                f"Unexpected closing tag </{tagname}>"
            ))

    def handle_comment(self, comment_text, line, char, endchar):
        self.handle_starttag(
            "comment", {"text": comment_text}, line, char, endchar
        )
        self.handle_closingtag("comment", line, char, endchar)

    def handle_doctype(self, doctype):
        self.doctype = doctype
        if doctype.startswith("avr/"):
            self.element_classes.extend([
                Pin,
                PinMode,
                DigitalWrite,
                DigitalRead
            ])
            if doctype == "avr/atmega328p":
                self.element_classes.extend([
                    SerialBegin,
                    SerialTransmit,
                    SerialPrint,
                    SerialReceive
                ])

    def handle_invalid_tag(self, line, char, endchar):
        self.diagnostics.append(Diagnostic(
            Severity.ERROR,
            CodeRange(self.dir, self.filename, line, char, line, endchar),
            f"Invalid tag"
        ))

    def new_element_by_tagname(self, tagname):
        """
        Creates an new element based on the tagname.
        tagname 'var' will return Var()
        tagname 'def' will return Def()
        tagname 'this-is-a-function-call' is not a known element so it
                                          will return FunctionCall()
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
                f"Unclosed element <{self.current_element.tagname}>\n"
                f"Did you mean <{self.current_element.tagname} "
                f"...attributes... /> ?"
            ))
