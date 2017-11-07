# app/Makefile -- A collection of rules for testing and deploying the project

DJANGO_PROJECT_ROOT=app

LINT_CMD=pylint
LINT_OPTIONS=--output-format=colorized --rcfile=.pylintrc

# Python source files to inspect for PEP8 compliance
LINT_TARGETS= \
	analysis/apps.py \
	analysis/models.py \
	analysis/urls.py \
	app/settings.py \
	app/urls.py \
	homepage/apps.py \
	homepage/urls.py \
	homepage/views.py \
	webtool/apps.py \
	webtool/forms.py \
	webtool/models.py \
	webtool/urls.py 

all: lint
deploy: collectstatic disabledebug
	systemctl --user restart EDAM

install:
	. ../venv/bin/activate
	pip install -r requirements.txt

disabledebug:
	sed -i -e 's/DEBUG\s*=\s*True/DEBUG = False/g' $(DJANGO_PROJECT_ROOT)/app/settings.py

collectstatic: install
	cd $(DJANGO_PROJECT_ROOT) && ./manage.py collectstatic --no-input

lint: $(LINT_TARGETS:%.py=$(DJANGO_PROJECT_ROOT)/%.py)
	$(LINT_CMD) $(LINT_OPTIONS) $^

test: install
	cd $(DJANGO_PROJECT_ROOT) && python manage.py test
