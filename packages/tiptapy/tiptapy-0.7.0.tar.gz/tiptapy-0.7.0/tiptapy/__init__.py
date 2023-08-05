import json

from html import escape as e
from typing import Dict
from inspect import isclass

__version__ = '0.7.0'

renderers: Dict = {}


class BaseNode:
    """
    Base Node class with reference implemention for common cases.
    This should be used as base class for all leaf level nodes
    which do not contain other nodes.
    """
    type = "prose-mirror_content-type"
    wrap_tag: str = ""

    def is_renderable(self, node):
        """
        Checks whether the node is worth rendering.
        Example: Image block without src attribute might not.
        """
        return True

    def render(self, in_data) -> str:
        out = ''
        if self.is_renderable(in_data):
            out = self.inner_render(in_data)
            if self.wrap_tag:
                out = f"<{self.wrap_tag}>{out}</{self.wrap_tag}>"
        return out

    def inner_render(self, node) -> str:
        return e(node["content"]["text"])


class BaseContainer(BaseNode):
    """
    Base class for container type nodes which may further contain other nodes.
    """

    def inner_render(self, nodes: Dict) -> str:
        out = ""
        for node in nodes.get("content", []):
            node_type = node.get("type")
            renderer = renderers.get(node_type)
            assert renderer, f'Unsupported node_type: "{node_type}"'
            if renderer:
                out += renderer.render(node)
        return out


class Text(BaseNode):
    type = "text"
    mark_tags = {"bold": "strong", "italic": "em", "link": "a"}

    def inner_render(self, node):
        text = e(node["text"])
        marks = node.get("marks")
        if marks:
            for mark in marks:
                tag = self.mark_tags.get(mark.get("type"))
                attrs = mark.get("attrs")
                if attrs:
                    attrs_s = " ".join(f'{k}="{e(v)}"' for k, v in attrs.items())
                    text = f"<{tag} {attrs_s}>{text}</{tag}>"
                else:
                    text = f"<{tag}>{text}</{tag}>"
        return text


class Heading(BaseContainer):
    type = "heading"

    def inner_render(self, node) -> str:
        attrs = node['attrs']
        level = attrs.get('level') or 1
        tag = e(f"h{level}")
        inner_html = super().inner_render(node)
        return f"<{tag}>{inner_html}</{tag}>"


class Image(BaseNode):
    type = "image"
    wrap_tag: str = "figure"

    def is_renderable(self, node):
        attrs = node.get("attrs", {})
        return bool(attrs.get('src', '').strip())


    def inner_render(self, node) -> str:
        special_attrs_map = {'caption': 'figcaption'}
        attrs = node.get("attrs", {})
        attrs_s = " ".join(f'{k}="{v}"'
                           for k, v in attrs.items()
                           if k not in special_attrs_map and v.strip()
                           )
        html = f"<img {attrs_s}>"
        caption = attrs.get('caption', '').strip()
        if caption:
            tag = special_attrs_map['caption']
            html += f"<{tag}>{e(caption)}</{tag}>"
        return html


class Embed(BaseContainer):
    type = "embed"

    def inner_render(self, node) -> str:
        attrs = node['attrs']
        html = attrs.get('html', '')
        if attrs.get('type') == 'video':
            caption = (attrs.get('caption') or '').strip()
            if caption:
                html += f"<figcaption>{caption}</figcaption>"
        provider_name = attrs.get('provider') or 'link'
        return f'<div class="embed-wrapper {provider_name.lower()}-wrapper"><figure>{html}</figure></div>'  # noqa: E501


class Title(BaseContainer):
    type = "title"
    wrap_tag: str = "h1"


class Paragraph(BaseContainer):
    type = "paragraph"
    wrap_tag: str = "p"


class BlockQuote(BaseContainer):
    type = "blockquote"
    wrap_tag: str = "blockquote"


class HardBreak(BaseContainer):
    type = "hard_break"

    def inner_render(self, node):
        return "<br>"


class HorizontalRule(BaseNode):
    type = "horizontal_rule"

    def inner_render(self, node):
        return "<hr>"


class ListItem(BaseContainer):
    type = "list_item"
    wrap_tag: str = "li"


class BulletList(BaseContainer):
    type = "bullet_list"
    wrap_tag: str = "ul"


class Doc(BaseContainer):
    type = "doc"


class OrderedList(BaseContainer):
    type = "ordered_list"
    wrap_tag: str = "ol"


def register_renderer(cls):
    renderers[cls.type] = cls()


for o in tuple(locals().values()):
    if isclass(o) and issubclass(o, BaseNode):
        register_renderer(o)


def convert_any(in_data):
    typ = in_data.get("type")
    renderer = renderers.get(typ)
    return renderer.render(in_data)


def to_html(s):
    in_data = s if isinstance(s, dict) else json.loads(s)
    return convert_any(in_data)


if __name__ == "__main__":
    import timeit

    s = open("tests/data.json").read()
    print(to_html(s))
    print(
        timeit.timeit(
            "to_html(s)",
            setup="from __main__ import to_html, s", number=100000
        )
    )
