from htmlc.elements.element import Element


class WhatIs(Element):

    def to_c(self, mapped_c):
        if not len(self.attributes):
            return
        key, attr = list(self.attributes.items())[0]
        val = attr.get("val") or (
            self.data.strip() if self.data else ""
        )
        mapped_c.add(
            f"#define {key} {val}\n", self
        )
