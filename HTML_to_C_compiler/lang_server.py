from json_rpc import JsonRpcServer


class LanguageServer(JsonRpcServer):

    def __init__(self):
        self.text_document__did_change = self.text_document__did_open

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

    def text_document__did_open(self, request):
        self.send({
            "method": "textDocument/publishDiagnostics",
            "params": {
                "uri": request["params"]["textDocument"]["uri"],
                "diagnostics": [
                    {
                        "range": {
                            "start": {"line": 0, "character": 0},
                            "end": {"line": 2, "character": 4}
                        },
                        "message": "shitty code",
                        "severity": 1
                    }
                ]
            }
        })


LanguageServer().start()
