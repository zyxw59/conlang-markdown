import re

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.util import etree

GLOSS_START = ':gloss:'

RE_WORD = re.compile(r'(\S+)|\{([^}]*)\}')

INDENT_LENGTH = 4

class GlossProcessor(BlockProcessor):
    """Processes interlinear glosses."""

    def test(self, parent, block):
        """A `gloss` block starts with `:gloss:` on a line by itself."""
        return block.split('\n')[0] == GLOSS_START

    def run(self, parent, blocks):
        """Parse a `gloss` block"""
        # split into lines, discarding the first line (which just contains the
        # tag)
        lines_raw = blocks.pop(0).split('\n')[1:]
        lines = []
        # last line of preamble
        pre = None
        # first line of postamble
        post = None
        # current line
        i = 0
        # iterate over raw lines, consolidating indented lines, and determining
        # the location of the pre- and post-amble
        for line in lines_raw:
            if lines and line.startswith(' ' * INDENT_LENGTH):
                # indented line; append to previous
                lines[-1] += line
            elif line.strip() == "::":
                # `::` alone on a line marks the end of the preamble or the
                # start of the postamble
                if pre == None:
                    pre = i
                elif post == None:
                    post = i
                else:
                    raise SyntaxError("Too many `::` in `gloss` block.")
            else:
                # append line and increment counter
                lines.append(line)
                i += 1
        # we need both a preamble and a postamble, tho both can be empty
        if pre == None or post == None:
            raise SyntaxError("Not enough `::` in `gloss` block.")
        div = etree.SubElement(parent, "div")
        div.set("class", "gloss")
        # preamble
        for line in lines[:pre]:
            par = etree.SubElement(div, "p")
            par.text = line
        # create columns for each word of the source
        columns = []
        for word in _parse_gloss_line(lines[pre]):
            dl = etree.SubElement(div, "dl")
            dt = etree.SubElement(dl, "dt")
            dt.text = word
            columns.append(dl)
        # iterate over subsequent lines
        for line in lines[pre+1:post]:
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
        # postamble
        for line in lines[post:]:
            par = etree.SubElement(div, "p")
            par.text = line


class GlossExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add("gloss", GlossProcessor(md.parser), "<paragraph")


def makeExtension(**kwargs):
    return GlossExtension(**kwargs)

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
    return y if x is None else x
