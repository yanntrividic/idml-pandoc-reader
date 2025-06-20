# Minimal makefile for Sphinx documentation
#

LOCALES         := en
LOCALEDIR       := locale
LOCALEFILES     := $(LOCALES:%=$(LOCALEDIR)/%/LC_MESSAGES/package.po) $(LOCALES:%=$(LOCALEDIR)/%/LC_MESSAGES/sphinx.po)
UPDATEPO        := $(filter update-po,$(MAKECMDGOALS))

DATE                := $(shell date +%F)
REVISION            := $(shell git describe --always --dirty --abbrev=4)
COPYRIGHT           := Yann Trividic

export AUTHORS      := $(shell awk '{printf t $$0; t=", "}' AUTHORS)
export PACKAGE      := Yann Trividic
export VERSION      := main
export RELEASE      := $(DATE)-g$(REVISION)
export EMAIL        := bonjour@yanntrividic.fr

export LOCALE       := fr
export LANGUAGES    := $(LOCALE) $(LOCALES)
export LATEXMKOPTS  := -file-line-error $(if $(CI),,-quiet)

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
