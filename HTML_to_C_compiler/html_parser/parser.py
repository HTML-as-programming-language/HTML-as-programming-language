import re


class HTMLParser:

    def feed(self, filepath):

        html = open(filepath).read()

        tags = self.split_html_by_tags(html)
        line = re.split(".+", html)[0].count("\n")  # number of empty lines at top of file
        for tag in tags:
            start_line = line + 1
            line += tag.count("\n")
            tag = tag.strip()

            if tag.isspace() or len(tag) == 0:
                continue

            tagname_and_attrs = tag[1:].split(">")[0]
            tagname = tagname_and_attrs.split(" ")[0].replace("/", "")
            data = tag.split(">")[1]

            if tagname == "!--":
                # woo its a comment
                self.handle_comment(tag[3:][:-3], start_line)
                if len(data) > 0 and not data.isspace():
                    self.handle_data(data, start_line)
                continue

            is_self_closing_tag = tagname_and_attrs.endswith("/")  # <p/> is a self closing tag
            is_closing_tag = tag.startswith("</")     # </p> is a closing tag

            if is_self_closing_tag:
                tag = tag[:-1]

            if not is_closing_tag:
                self.handle_starttag(tagname, self.parse_attrs(tagname_and_attrs), start_line)
            elif is_closing_tag:
                self.handle_closingtag(tagname, start_line)

            if is_self_closing_tag:
                self.handle_closingtag(tagname, start_line)

            if len(data) > 0 and not data.isspace():
                self.handle_data(data, start_line)

        self.finish_parsing()

    def parse_attrs(self, tagname_and_attrs):
        if tagname_and_attrs.endswith("/"):
            tagname_and_attrs = tagname_and_attrs[:-1]

        attr_strings = re.split(" |\n", tagname_and_attrs)
        del attr_strings[0]     # the tagname is not an attribute

        if len(attr_strings) == 0:
            return {}

        # combine multi-line strings into 1 attribute:
        for i in range(len(attr_strings) - 1, 0, -1):
            attr_str = attr_strings[i]
            if attr_str.count('"') == 1:
                del attr_strings[i]
                attr_strings[i - 1] += attr_str

        attrs = {}
        for attr_str in attr_strings:
            splitted = attr_str.split("=")
            key = splitted[0]
            val = splitted[1] if len(splitted) == 2 else None

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

    def split_html_by_tags(self, html):
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

            if char == "<" and i < len(html) - 1:
                valid_opening_tag = not in_string and not html[i + 1].isspace()
                if valid_opening_tag:
                    split_at_indices.append(i)

        return [html[i:j] for i,j in zip(split_at_indices, split_at_indices[1:]+[None])]

    def handle_comment(self, comment_text, line):
        pass

    def handle_starttag(self, tagname, attrs, line):
        pass

    def handle_data(self, data, line):
        pass

    def handle_closingtag(self, tagname, line):
        pass

    def finish_parsing(self):
        pass
