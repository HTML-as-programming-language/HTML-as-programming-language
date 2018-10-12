from json_rpc import JsonRpcServer


class LanguageServer(JsonRpcServer):

    def initialize(self, request):
        self.respond(request, {
            "capabilities": {}
        })


LanguageServer().start()
