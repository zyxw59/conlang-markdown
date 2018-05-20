from pathlib import Path

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree

class DocumentGenerator(Treeprocessor):
    """Produces a self-contained HTML document."""

    def __init__(self, md, css_path="", stylesheets=None):
        self.md = md
        self.css_path = Path(css_path)
        self.stylesheets = stylesheets or []
        super().__init__(md)

    def run(self, root):
        html = etree.Element("html")
        head = etree.SubElement(html, "head")
        etree.SubElement(head, "meta", charset="utf-8").tail = "\n"
        for style in self.stylesheets:
            etree.SubElement(
                    head,
                    "link",
                    rel="stylesheet",
                    href=str(self.css_path.joinpath(style).with_suffix(".css"))
                    ).tail = "\n"
        title = etree.SubElement(head, "title")
        title.text = _first(root.findall("h1")).text
        title.tail = "\n"
        body = etree.SubElement(html, "body")
        # for pretty printing
        html.text = "\n"
        head.text = "\n"
        head.tail = "\n"
        body.text = "\n"
        body.tail = "\n"
        # append the existing document
        body.append(root)
        # don't strip away what we just added to the tree:
        self.md.stripTopLevelTags = False
        return html

class DocumentExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
                "css_path": ["", "Path to css stylesheets"],
                "stylesheets": [[], "Stylesheets to include"],
                }
        super().__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add(
                "document",
                DocumentGenerator(md, **self.getConfigs()),
                "_end")


def makeExtension(**kwargs):
    return DocumentExtension(**kwargs)


def _first(it):
    """Returns the first element of an iterator or list."""
    try:
        return it[0]
    except TypeError:
        return next(it)
