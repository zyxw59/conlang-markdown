import re

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.util import etree

GLOSS_START = ':gloss:'

RE_WORD = re.compile(r'(\w+)|\{([^}]*)\}')

class GlossProcessor(BlockProcessor):
    """Processes interlinear glosses."""

    def test(self, parent, block):
        """A `gloss` block starts with `:gloss:` on a line by itself."""
        return block.split('\n')[0] == GLOSS_START

    def run(self, parent, blocks):
        """Parse a `gloss` block"""
        # split into lines, discarding the first line (which just contains the
        # tag)
        lines = blocks.pop(0).split('\n')[1:]
        div = etree.SubElement(parent, "div")
        div.attrib["class"] = "gloss"
        columns = []
        # create columns for each word of the source
        for word in _parse_gloss_line(lines[0]):
            dl = etree.SubElement(div, "dl")
            dt = etree.SubElement(dl, "dt")
            dt.text = word
            columns.append(dl)
        # iterate over subsequent lines
        for line in lines[1:]:
            words = _parse_gloss_line(line)
            # iterate over columns
            for i, dl in enumerate(columns):
                if i < len(words):
                    # if this line has a word in this column, add it
                    dd = etree.SubElement(dl, "dd")
                    dd.text = words[i]
                else:
                    # otherwise, add an empty `<dd>` element
                    etree.SubElement(dl, "dd")


class GlossExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add("gloss", GlossProcessor(md.parser), "<paragraph")


def _parse_gloss_line(line):
    """
    Parses a line of a gloss, separating it into words.

    Words are separated by spaces, except when contained by curly braces.
    """
    return [_whichever(*word.groups()) for word in RE_WORD.finditer(line)]

def _whichever(x, y):
    """Returns whichever of `x` and `y` is not `None`.

    If both `x` and `y` are not `None`, returns `x`.

    If both `x` and `y` are `None`, returns `None`.
    """
    y if x is None else x
