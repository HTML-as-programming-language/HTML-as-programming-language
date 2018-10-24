import os
import shutil
import traceback


def __caller_name__():
    return traceback.extract_stack(None, 2)[0][-2]


def restore_working_code(func):
    def func_wrapper():
        backup("working-code", func.__name__)
        func()
        restore("working-code", func.__name__)

    return func_wrapper


def backup(folder, env_name="tmp"):
    new_folder = folder + "-" + env_name
    if os.path.isdir(new_folder):
        delete(new_folder)

    shutil.copytree(folder, new_folder)
    return new_folder


def delete(env_str):
    shutil.rmtree(env_str)


def restore(folder, env_name="tmp"):
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

    return len(differences) == 0 + do_not_count
