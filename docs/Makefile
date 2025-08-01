# Minimal makefile for Sphinx documentation
#

LOCALES         := en
LOCALEDIR       := locale

export LOCALE       := fr
export LANGUAGES    := $(LOCALE) $(LOCALES)

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: all
all: $(LANGUAGES)

.PHONY: $(LANGUAGES)
$(LANGUAGES):
	@echo "Building language: $@"
	@$(SPHINXBUILD) -b html -D language=$@ $(SPHINXOPTS) $(SOURCEDIR) $(BUILDDIR)/$@
	cp $(SOURCEDIR)/.htaccess $(BUILDDIR)/.htaccess
	cp $(SOURCEDIR)/custom_404_handler.php $(BUILDDIR)/custom_404_handler.php

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	