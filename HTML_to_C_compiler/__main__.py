import sys

from htmlc import compiler

from htmlc.lang_server import LanguageServer

if "langsvr" in sys.argv:
    LanguageServer().start()

elif "htmlc" in sys.argv:
    compiler.main()
