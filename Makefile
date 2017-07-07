# app/Makefile -- A collection of rules for testing and deploying the project

DJANGO_PROJECT_ROOT=app

LINT_CMD=pylint
LINT_OPTIONS=--output-format=colorized --rcfile=.pylintrc
# Space-separated Python source files to inspect for PEP8 compliance
LINT_TARGETS=webtool/apps.py

all: lint 

lint: $(LINT_TARGETS:%.py=$(DJANGO_PROJECT_ROOT)/%.py)
	$(LINT_CMD) $(LINT_OPTIONS) $^

test:
	cd $(DJANGO_PROJECT_ROOT) && python2 manage.py test
