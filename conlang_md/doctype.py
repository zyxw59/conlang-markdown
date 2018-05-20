from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor

class DoctypeProcessor(Postprocessor):
    def __init__(self, doctype="html"):
        self.doctype = doctype

    def run(self, text):
        return f"<!DOCTYPE {self.doctype}>\n{text}"


class DoctypeExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            "doctype": ["html", "the doctype string to include"],
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add(
                "doctype",
                DoctypeProcessor(**self.getConfigs()),
                "_end")

def makeExtension(*args, **kwargs):
    return DoctypeExtension(*args, **kwargs)
