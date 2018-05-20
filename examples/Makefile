EXTENSIONS=conlang_md.gloss\
	   conlang_md.smallcaps\
	   conlang_md.document\
	   conlang_md.doctype

CONFIG_FILE=example_config.yaml

MARKDOWN=python3.6 -m markdown

example.html: example.md $(CONFIG_FILE)
	$(MARKDOWN) -c $(CONFIG_FILE) $(patsubst %, -x %, $(EXTENSIONS)) $< > $@
