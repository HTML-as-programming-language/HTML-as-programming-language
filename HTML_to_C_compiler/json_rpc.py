# https://microsoft.github.io/language-server-protocol/specification
import sys
import re
import json

from utils import camel_case_to_snake


class JsonRpcServer:

    def start(self):
        """
        Listen for requests that look like this:

        Content-Length: ...

        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "textDocument/didOpen",
            "params": {
                ...
            }
        }
        """
        buffer = ""
        content_len = 0
        while True:
            buffer += sys.stdin.read(1)
            if not content_len:

                if re.match("Content-Length: \d+\n\n", buffer):
                    started = True
                    content_len = int(buffer.split(": ")[1].split("\r")[0])
                    buffer = ""

            else:
                if len(buffer) == content_len:
                    self.handle(json.loads(buffer))
                    content_len = 0
                    buffer = ""

    def handle(self, request):
        if "method" in request:
            method_name = camel_case_to_snake(request["method"].replace("/", "__"))
            if method_name in dir(self):
                self.__getattribute__(method_name)(request)

    def respond(self, request, response):
        self.send({
            "id": request["id"],
            "result": response
        })

    def send(self, something):
        something["jsonrpc"] = "2.0"
        content = json.dumps(something, separators=(",", ":"))

        s = (
            "Content-Length: {}\r\nContent-Type: application/vscode-jsonrpc; charset=utf8\r\n\r\n{}"
                .format(len(content), content)
        )

        sys.stdout.buffer.write(bytearray(s, "utf-8"))
        sys.stdout.flush()
