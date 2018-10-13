import os
import re
from urllib import parse, request as urlreq
from htmlc import utils

from htmlc.html_parser import HTMLParser
from htmlc.lexer import Lexer
from htmlc.diagnostics import diagnose
from htmlc.json_rpc import JsonRpcServer
from htmlc.linker import Linker


class LanguageServer(JsonRpcServer):

    def __init__(self):
        self.text_document__did_open = self.text_document__did_change

    def initialize(self, request):
        self.respond(request, {
            "capabilities": {
                "textDocumentSync": 1  # 0 = None, 1 = full, 2 = incremental
            }
        })
        self.send({
            "method": "window/showMessage",
            "params": {
                "type": 3,
                "message": "HTMLC Language Server started"
            }
        })

    def text_document__did_change(self, request):

        params = request["params"]
        uri = params["textDocument"]["uri"]

        filepath = parse.urlparse(uri).path
        filepath = urlreq.url2pathname(filepath)
        if re.match("\\\\[a-zA-Z]:\\\\", filepath):
            # user is on windows, remove backslash before drive-letter
            filepath = filepath[1:]

        if filepath.endswith(".git"):
            filepath = filepath.split(".git")[0]

        lexer = Lexer(utils.file_dir(filepath), utils.filename(filepath))
        parser = HTMLParser()

        if "contentChanges" in params and len(params["contentChanges"]):
            parser.feed(lexer, html=params["contentChanges"][0]["text"])
        else:
            parser.feed(lexer, filepath=filepath)

        element_tree = lexer.elements

        linker = Linker(element_tree, parser)
        linker.link_external_files()

        for el in element_tree:
            el.init()
            el.init_children()

        diagnostics = diagnose(element_tree)
        diagnostics.extend(linker.diagnostics)
        diagnostics.extend(lexer.diagnostics)

        self.send({
            "method": "textDocument/publishDiagnostics",
            "params": {
                "uri": uri,
                "diagnostics": [
                    d.to_json()
                    for d in diagnostics
                    if os.path.abspath(d.code_range.dir + d.code_range.filename) == filepath
                ]
            }
        })


if __name__ == "__main__":
    LanguageServer().start()
