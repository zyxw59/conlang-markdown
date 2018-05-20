from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree

RE_SMALL_CAPS = r"\^\^([^\^]+)\^\^"

class SmallCapsPattern(Pattern):
    def __init__(self):
        super().__init__(RE_SMALL_CAPS)

    def handleMatch(self, m):
        span = etree.Element("span")
        span.set("class", "small-caps")
        span.text = m.group(2)
        return span

class SmallCapsExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add(
                "smallcaps",
                SmallCapsPattern(),
                '<not_strong')

def makeExtension(**kwargs):
    return SmallCapsExtension(**kwargs)
