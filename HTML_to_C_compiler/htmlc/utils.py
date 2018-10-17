import os
import re


def camel_case_to_snake(text):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def camel_case_to_hyphenated(text):
    """"
    CamelCase -> camel-case
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


def hyphenated_to_camel_case(text):
    """"
    camel-case -> camelCase
    """
    first, *rest = text.split("-")
    return first + ''.join(word.capitalize() for word in rest)


def remove_indentation(text):
    """
    removes indentation from a multi line string
    """
    return "".join("{}\n".format(x.strip()) for x in text.split("\n"))


def indent(text, tabs):
    """
    indents text
    """
    return "".join("{}{}\n".format("    " * tabs, x) for x in text.split("\n"))


def file_dir(filepath):
    filepath = os.path.abspath(filepath)
    reversed = filepath[::-1]
    splitted = re.split("\/|\\\\", reversed, 1)
    if len(splitted) == 1:
        return "./"
    return splitted[1][::-1] + "/"


def filename(filepath):
    return re.split("\/|\\\\", filepath[::-1], 1)[0][::-1]


def split_preserve_substrings(string, separator):
    if len(string) == 0:
        return [""]
    splitted = []
    in_sub_string = False
    opening_char = None
    length = len(string)
    sep_len = len(separator)

    prev_i = 0
    for i in range(len(string)):
        char = string[i]
        is_last = i == length - 1
        if char == "'" or char == '"':
            if char == opening_char:
                in_sub_string = False
            else:
                in_sub_string = True
                opening_char = char

        if in_sub_string and not is_last:
            continue

        found_sep = string[i:i+sep_len] == separator
        if found_sep or is_last:
            splitted.append(
                string[
                    (prev_i + sep_len if prev_i > 0 else 0):(i if found_sep else i + 1)
                ]
            )
            prev_i = i
    return splitted


#returns the content of a file
def includeFile(filepath):
    file = open(filepath, "r")
    content = file.read()
    file.close()
    return content
