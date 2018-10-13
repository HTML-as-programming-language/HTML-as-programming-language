import sys

from htmlc.lang_server import LanguageServer

if "langsvr" in sys.argv:
    LanguageServer().start()
