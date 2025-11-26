ifdef CIRCLECI
	RUN := pipenv run
else ifdef HEROKU_APP_NAME
	SKIP_INSTALL := true
else
	RUN := pipenv run
endif

.PHONY: all
all: check test ## CI | Run all validation targets

.PHONY: dev
dev: install ## CI | Rerun all validation targests in a loop
	@ rm -rf $(FAILURES)
	$(RUN) sniffer

# SYSTEM DEPENDENCIES #########################################################

.PHONY: doctor
doctor: ## Check for required system dependencies
	bin/verchew --exit-code

# PROJECT DEPENDENCIES ########################################################

export PIPENV_VENV_IN_PROJECT=true
VENV := .venv

BACKEND_DEPENDENCIES := $(VENV)/.pipenv-$(shell bin/checksum Pipfile*)
FRONTEND_DEPENDENCIES :=

.PHONY: install
ifndef SKIP_INSTALL
install: $(BACKEND_DEPENDENCIES) $(FRONTEND_DEPENDENCIES) ## Install project dependencies
endif

$(BACKEND_DEPENDENCIES):
	@if [ ! -d "$(VENV)" ]; then \
		pipenv install --python 3.9 --skip-lock || pipenv --python 3.9; \
	fi
	pipenv run pip install PyYAML==6.0.3 || true
	pipenv run pip install YORM==1.6.2 --no-deps || true
	pipenv run pip install "parse~=1.8.0" "pathlib2!=2.3.3" simplejson || true
	pipenv install --dev --skip-lock
	pipenv run pip install --upgrade --force-reinstall PyYAML==6.0.3
	@ touch $@

$(FRONTEND_DEPENDENCIES):
	@ touch $@

.PHONY: clean
clean:
	rm -rf staticfiles
	rm -rf .coverage htmlcov

.PHONY: clean-all
clean-all: clean
	rm -rf $(VENV)

# RUNTIME DEPENDENCIES ########################################################

data:
	rm -rf /tmp/data
	mkdir -p /tmp/data
	cd /tmp/data && git init --bare
	git clone /tmp/data data
	cd data && git config user.name "Test User"
	cd data && git config user.email "test@example.com"
	cd data && git checkout -b master
	cd data && git commit --allow-empty --message "Initial commit"
	cd data && git push --set-upstream origin master
	cd data && git push && git pull

# VALIDATION TARGETS ##########################################################

PYTHON_PACKAGES := api
FAILURES := .cache/v/cache/lastfailed

.PHONY: check
check: check-backend ## Run static analysis

.PHONY: check-backend
check-backend: install
	$(RUN) pylint $(PYTHON_PACKAGES) tests --rcfile=.pylint.ini
	$(RUN) pycodestyle $(PYTHON_PACKAGES) tests --config=.pycodestyle.ini

.PHONY: check-frontend
check-frontend: install

.PHONY: test
test: test-backend test-frontend ## Run all tests

.PHONY: test-backend
test-backend: test-backend-all

.PHONY: test-backend-unit
test-backend-unit: install data
	@ ( mv $(FAILURES) $(FAILURES).bak || true ) > /dev/null 2>&1
	$(RUN) pytest $(PYTHON_PACKAGES) tests/unit
	@ ( mv $(FAILURES).bak $(FAILURES) || true ) > /dev/null 2>&1
	$(RUN) coveragespace update unit

.PHONY: test-backend-integration
test-backend-integration: install data
	@ if test -e $(FAILURES); then $(RUN) pytest tests/integration; fi
	@ rm -rf $(FAILURES)
	$(RUN) pytest tests/integration
	$(RUN) coveragespace update integration

.PHONY: test-backend-all
test-backend-all: install data
	@ if test -e $(FAILURES); then $(RUN) pytest $(PYTHON_PACKAGES) tests/integration; fi
	@ rm -rf $(FAILURES)
	$(RUN) pytest $(PYTHON_PACKAGES) tests/integration
	$(RUN) coveragespace update overall

.PHONY: test-frontend
test-frontend: test-frontend-unit

.PHONY: test-frontend-unit
test-frontend-unit: install

.PHONY: test-system
test-system: install
	$(RUN) honcho start --procfile=tests/system/Procfile --env=tests/system/.env

# SERVER TARGETS ##############################################################

export FLASK_APP=api/app.py

.PHONY: run
run: install data ## Run the applicaiton
	FLASK_ENV=local $(RUN) python manage.py runserver

.PHONY: run-production
run-production: install ## Run the application (simulate production)
	pipenv shell "bin/pre_compile; exit \$$?"
	pipenv shell "bin/post_compile; exit \$$?"
	pipenv shell "heroku local release; exit \$$?"
	pipenv shell "FLASK_ENV=production heroku local web; exit \$$?"

# RELEASE TARGETS #############################################################

MKDOCS_INDEX := site/index.html

.PHONY: promote
promote: install
	TEST_SITE=https://staging.coverage.space $(RUN) pytest tests/system --cache-clear
	heroku pipelines:promote --app coverage-space-staging --to coverage-space
	TEST_SITE=https://api.coverage.space $(RUN) pytest tests/system

.PHONY: mkdocs
mkdocs: install $(MKDOCS_INDEX)
$(MKDOCS_INDEX): mkdocs.yml docs/*.md
	ln -sf `realpath CHANGELOG.md --relative-to=docs/about` docs/about/changelog.md
	ln -sf `realpath CONTRIBUTING.md --relative-to=docs/about` docs/about/contributing.md
	ln -sf `realpath LICENSE.md --relative-to=docs/about` docs/about/license.md
	pipenv run mkdocs build --clean --strict
	echo coverage.space > site/CNAME

# HELP ########################################################################

.PHONY: help
help: install
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
