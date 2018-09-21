import re


class HTMLParser:

    def feed(self, filepath):

        html = open(filepath).read()

        elements = html.split("<")
        line = 0
        for el in elements:
            start_line = line + 1
            line += el.count("\n")
            el = el.strip()

            if el.isspace() or len(el) == 0:
                continue

            tag = el.split(">")[0]
            tagname = tag.split(" ")[0].replace("/", "")
            data = el.split(">")[1]

            if tagname == "!--":
                # woo its a comment
                self.handle_comment(tag[3:][:-3], start_line)
                if len(data) > 0 and not data.isspace():
                    self.handle_data(data, start_line)
                continue

            is_self_closing_tag = tag.endswith("/")  # <p/> is a self closing tag
            is_closing_tag = tag.startswith("/")     # </p> is a closing tag

            if is_self_closing_tag:
                tag = tag[:-1]

            if not is_closing_tag:
                self.handle_starttag(tagname, self.parse_attrs(tag), start_line)
            elif is_closing_tag:
                self.handle_closingtag(tagname, start_line)

            if is_self_closing_tag:
                self.handle_closingtag(tagname, start_line)

            if len(data) > 0 and not data.isspace():
                self.handle_data(data, start_line)

        self.finish_parsing()

    def parse_attrs(self, tag):
        attr_strings = re.split(" |\n", tag)
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
