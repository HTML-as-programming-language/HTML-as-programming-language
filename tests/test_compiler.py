# import sys
# sys.path.append("..")

from htmlc import compiler
from unittest.mock import patch
import sys
import os
from pathlib import Path
import traceback
import shutil

from pprint import pprint


def __caller_name__():
    return traceback.extract_stack(None, 2)[0][-2]



def restore_working_code(func):
    def func_wrapper():
        backup_enviorment("working-code", func.__name__)
        func()
        restore_enviorment("working-code", func.__name__)

    return func_wrapper


def backup_enviorment(folder, env_name="tmp"):
    new_folder = folder + "-" + env_name
    if os.path.isdir(new_folder):
        delete_enviorment(new_folder)

    shutil.copytree(folder, new_folder)
    return new_folder


def delete_enviorment(env_str):
    shutil.rmtree(env_str)


def restore_enviorment(folder, env_name="tmp"):
    new_folder = folder + "-" + env_name
    shutil.rmtree(folder)
    shutil.copytree(new_folder, folder)
    shutil.rmtree(new_folder)

def files_look_alike(nr1, nr2):
    with open(nr1, 'r') as file1:
        with open(nr2, 'r') as file2:
            differences = set(file1).difference(file2)

    differences.discard(' ')
    differences.discard('\t')
    differences.discard('\n')

    do_not_count = 0
    for difference in differences:
        if str(difference).replace(" ", "").replace("\t", "").startswith("//"):
            do_not_count += 1

    pprint(differences)
    return len(differences) == 0 + do_not_count


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

    pathlist = Path("working-code").glob('**/*.html')
    for path in pathlist:
        with patch.object(sys, 'argv', [str(path)]):
            compiler.main()

        out_str = "working-code/out/" + str(path).split("/")[-1].replace(".html",  ".c")
        assert Path(out_str).is_file()


def test_working_code_equals():
    """
    Test if the working code folder compiles
    """

    enviorment_str = backup_enviorment("working-code", "backup")

    pathlist = Path(enviorment_str).glob('**/*.html')
    for path in pathlist:
        with patch.object(sys, 'argv', [str(path)]):
            compiler.main()

        out_str = enviorment_str + "/out/" + str(path).split("/")[-1].replace(".html",  ".c")
        backup_str = out_str.replace(enviorment_str, "working-code")
        assert files_look_alike(out_str, backup_str)

    delete_enviorment(enviorment_str)


def test_compiler_file_not_found(capsys):
    @restore_working_code
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