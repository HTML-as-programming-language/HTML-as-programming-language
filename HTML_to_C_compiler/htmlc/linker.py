import os

from htmlc import utils
from htmlc.diagnostics import Diagnostic, Severity
from htmlc.lexer import Lexer


class Linker:

    def __init__(self, element_tree, html_parser):
        self.element_tree = element_tree
        self.html_parser = html_parser
        self.linked = [
            os.path.abspath(element_tree[0].code_range.dir + element_tree[0].code_range.filename)
            if len(element_tree) > 0 else None
        ]
        self.diagnostics = []

    def link_external_files(self):

        self.__loop_trough_elements__(self.element_tree)

    def __loop_trough_elements__(self, elements):
        for el in elements:
            if el.tagname != "script" and el.tagname != "link":
                self.__loop_trough_elements__(el.children)
                continue

            link_type = el.attributes.get("type", {}).get("val")
            if link_type != "text/html":
                continue

            src_attr_name = "src" if el.tagname == "script" else "href"
            src = el.attributes.get(src_attr_name, {}).get("val")
            if not src:
                self.diagnostics.append(Diagnostic(
                    Severity.ERROR,
                    el.code_range,
                    "Found {} element without {} attribute".format(el.tagname, src_attr_name)
                ))
                return
            self.__link__(src, el)
            self.__loop_trough_elements__(el.children)

    def __link__(self, file, link_element):

        path = os.path.abspath(link_element.code_range.dir + file)

        if path in self.linked:
            return

        self.linked.append(path)

        try:
            open(path)
        except FileNotFoundError:
            self.diagnostics.append(Diagnostic(
                Severity.WARNING,
                link_element.code_range,
                "'{}' not included, file was not found".format(file)
            ))
            return

        lexer = Lexer(utils.file_dir(path), utils.filename(path))
        self.html_parser.feed(path, lexer)
        link_element.children = lexer.elements
        self.diagnostics.extend(lexer.diagnostics)
