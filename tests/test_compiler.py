# import sys
# sys.path.append("..")

from htmlc import compiler
from unittest.mock import patch
import sys
from pathlib import Path
import traceback
import shutil

def __caller_name__():
    return traceback.extract_stack(None, 2)[0][-2]


def restore_working_code(func):
    def func_wrapper():
        backup_enviorment("working-code", func.__name__)
        func()
        restore_enviorment("working-code", func.__name__)

    return func_wrapper


def backup_enviorment(folder, env_name="tmp"):
    shutil.copytree(folder, folder + "-" + env_name)


def delete_enviorment(folder, env_name="tmp"):
    shutil.rmtree(folder + "-" + env_name)


def restore_enviorment(folder, env_name="tmp"):
    shutil.rmtree(folder)
    shutil.copytree(folder + "-" + env_name, folder)
    shutil.rmtree(folder + "-" + env_name)



def test_empty(capsys):
    """
    Give an error when no .html file is given in
    """
    compiler.main()

    captured = capsys.readouterr()
    assert "Please" in captured.out and ".html" in captured.out


@restore_working_code
def test_working_code_compile():
    """
    Test if the working code folder compiles
    """

    pathlist = Path("working_code").glob('**/*.html')
    for path in pathlist:
        path_in_str = str(path)
        with patch.object(sys, 'argv', [str(path_in_str)]):
            compiler.main()

        out_str = "working_code/out/" + path_in_str.split("/")[-1].replace(".html",  ".c")
        assert Path(out_str).is_file()
