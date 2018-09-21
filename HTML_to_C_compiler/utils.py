import re


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

