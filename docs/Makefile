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