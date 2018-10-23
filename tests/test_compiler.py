# import sys
# sys.path.append("..")

from htmlc import compiler
from unittest.mock import patch
import sys
from pathlib import Path



def test_empty(capsys):
    """
    Give an error when no .html file is given in
    """
    compiler.main()

    captured = capsys.readouterr()
    assert "Please" in captured.out and ".html" in captured.out


def test_working_code():
    """
    Test if the working code folder compiles
    """
    pathlist = Path("working-code").glob('**/*.html')
    for path in pathlist:
        path_in_str = str(path)
        with patch.object(sys, 'argv', [str(path_in_str)]):
            compiler.main()

        out_str = "working-code/out/" + path_in_str.split("/")[-1].replace(".html",  ".c")
        assert Path(out_str).is_file()
