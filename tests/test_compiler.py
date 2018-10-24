# import sys
# sys.path.append("..")

from htmlc import compiler
from unittest.mock import patch
import sys
from pathlib import Path
from test_helpers import enviorment


def test_empty(capsys):
    """
    Give an error when no .html file is given in
    """
    compiler.main()

    captured = capsys.readouterr()
    assert "Please" in captured.out and ".html" in captured.out


@enviorment.restore_working_code
def test_working_code_compile():
    """
    Test if the working code folder compiles
    """
    pathlist = Path("working-code").glob('**/*.html')
    for path in pathlist:
        with patch.object(sys, 'argv', [str(path)]):
            compiler.main()

        out_str = "working-code/out/" + str(path).split("/")[-1].replace(".html",  ".c")
        assert Path(out_str).is_file()


def test_working_code_equals():
    """
    Test if the working code folder equals the code that is currently on the github repo
    """
    enviorment_str = enviorment.backup("working-code", "backup")

    pathlist = Path(enviorment_str).glob('**/*.html')
    for path in pathlist:
        with patch.object(sys, 'argv', [str(path)]):
            compiler.main()

        out_str = enviorment_str + "/out/" + str(path).split("/")[-1].replace(".html",  ".c")
        backup_str = out_str.replace(enviorment_str, "working-code")
        assert enviorment.files_look_alike(out_str, backup_str)

    enviorment.delete(enviorment_str)


def test_compiler_file_not_found(capsys):
    """
    Test if wrong file paths cause an error
    """
    @enviorment.restore_working_code
    def test_compiler_file_not_found_inner():
        items = [
            "http://www.cs.uu.nl/docs/vakken/magr/portfolio/index.html",
            "/random/fake/../fake2/../fake3/index.html",
            "random.c",
        ]
        for item in items:
            with patch.object(sys, 'argv', [item]):
                compiler.main()

                captured = capsys.readouterr()
                assert "File not found:" in captured.out or ("Please" in captured.out and ".html" in captured.out)

    test_compiler_file_not_found_inner()