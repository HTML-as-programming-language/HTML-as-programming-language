import re

from htmlc.utils import split_preserve_substrings


class HTMLParser:
    """
    The HTML parser reads the HTML file that is given in feed()
    While it reads the HTML file it will call several methods of the handler:

        - handle_starttag() when it encounters a start-tag like <var a=5>

        - handle_data() when it encounters text/data inside an element like ..>data here</..

        - handle_closingtag() when it encounters a closing-tag like </var>

        - handle_comment() when it encounters a comment like <!-- hello -->

        - finish_parsing() when it is done reading the file
    """

    class Handler:

        def handle_comment(self, comment_text, line, char, endchar):
            pass

        def handle_starttag(self, tagname, attrs, line, char, endchar):
            pass

        def handle_data(self, data, line):
            pass

        def handle_closingtag(self, tagname, line, char, endchar):
            pass

        def finish_parsing(self):
            pass

        def handle_doctype(self, doctype):
            pass

    def feed(self, filepath, handler):
        """
        call this to start reading a HTML file
        :param handler:
        :param filepath: for example: "../working-code.html"
        """

        html = open(filepath).read()

        tags = self.__split_html_by_tags__(html)
        line = re.split(".+", html)[0].count("\n")  # number of empty lines at top of file
        char = 0
        line_len = 0
        for tag in tags:
            start_line = line + 1
            new_lines = tag.count("\n")
            line += new_lines
            char = 0 if new_lines > 0 else line_len
            line_len = len(tag)
            endchar = char + line_len
            tag = tag.strip()

            if tag.isspace() or len(tag) == 0:
                continue

            tagname_and_attrs = split_preserve_substrings(tag[1:], ">")[0]
            tagname = split_preserve_substrings(tagname_and_attrs, " ")[0].replace("/", "")

            if tagname == "!--":    # found a comment
                handler.handle_comment(tag[4:][:-3], start_line, char, endchar)
                continue
            elif tagname.lower() == "!doctype":     # found a doctype-tag
                handler.handle_doctype(tag)
                continue

            data = tag.split(">")[1]

            is_self_closing_tag = tagname_and_attrs.endswith("/")   # <p/> is a self closing tag
            is_closing_tag = tag.startswith("</")                   # </p> is a closing tag

            if is_self_closing_tag:
                tag = tag[:-1]

            if not is_closing_tag:
                handler.handle_starttag(
                    tagname, self.__parse_attrs__(tagname_and_attrs), start_line, char, endchar
                )
            elif is_closing_tag:
                handler.handle_closingtag(tagname, start_line, char, endchar)

            if is_self_closing_tag:
                handler.handle_closingtag(tagname, start_line, char, endchar)

            if len(data) > 0 and not data.isspace():
                handler.handle_data(data, start_line)

        handler.finish_parsing()

    def __parse_attrs__(self, tagname_and_attrs):
        """
        This function will parse the attributes of a tag
        (this function should only be used by the HTML parser itself, aka 'private' in java)

        :param tagname_and_attrs: for example: 'var a=5 hello="hey"/'
        :return: dict of attributes, for example: {a: {val: 5, type='int'}, hello: {val: 'hey', type: 'String'}}
        """

        if tagname_and_attrs.endswith("/"):
            tagname_and_attrs = tagname_and_attrs[:-1]

        attr_strings = "\n".join(split_preserve_substrings(tagname_and_attrs, " "))
        attr_strings = split_preserve_substrings(attr_strings, "\n")
        del attr_strings[0]     # the tagname is not an attribute

        if len(attr_strings) == 0:
            return {}

        attrs = {}
        for attr_str in attr_strings:
            splitted = attr_str.split("=", maxsplit=1)
            key = splitted[0]
            val = splitted[1].replace("\n", "\\n") if len(splitted) == 2 else None

            if val is None:
                type = None
            elif val.startswith("'") and val.endswith("'"):
                type = "char"
                val = val[1:2][0]
            elif val.startswith('"') and val.endswith('"'):
                type = "String"
                val = val[1:-1]
            elif "." in val and val.replace(".", "").isdigit():
                type = "float"
                val = float(val)
            elif val.isnumeric():
                type = "int"
                val = int(val)
            else:
                type = "unknown"

            attrs[key] = {
                "type": type,
                "val": val
            }
        return attrs

    def __split_html_by_tags__(self, html):
        in_comment = False
        in_string = False
        string_quotes = '"'
        split_at_indices = []

        for i in range(len(html)):
            char = html[i]
            if char == '"' or char == "'":
                if in_string and string_quotes == char:
                    in_string = False
                elif not in_string:
                    in_string = True
                    string_quotes = char

            opening_of_comment = html[i:i+4] == "<!--"
            if opening_of_comment:
                in_comment = True
            elif in_comment and html[i:i+3] == "-->":
                in_comment = False
            if char == "<" and i < len(html) - 1:
                next_char = html[i + 1]
                valid_opening_tag = (
                    not in_string
                    and not next_char.isspace()
                    and not next_char == "="
                    and not (in_comment and not opening_of_comment)
                )
                if valid_opening_tag:
                    split_at_indices.append(i)

        return [html[i:j] for i,j in zip(split_at_indices, split_at_indices[1:]+[None])]
