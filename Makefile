PYTHON=$$(which python3)
PIP=$$(which pip3)
PROJECT_NAME=musical_games
PROJECT_VERSION=$$($(PYTHON) setup.py --version)

.PHONY: help
help:
	@echo "clean - remove all build, test, coverage and Python artifacts (no uninstall)"
	@echo "lint - check style with flake8"
	@echo "test(s)- run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "docs-pdf - generate the PDF documentation, including API docs"
	@echo "docs-man - generate the linux manpages"
	@echo "docs-changelog - generate the changelog documentation"
	@echo "prepare-release - prepare for a new release"
	@echo "release - package and upload a release"
	@echo "dist - create a pip package"
	@echo "install - installs the package using pip"
	@echo "uninstall - uninstalls the package using pip"

.PHONY: clean
clean: clean-build clean-pyc clean-test
	$(PYTHON) setup.py clean

.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

.PHONY: lint
lint:
	flake8 $(PROJECT_NAME) tests

.PHONY: test
test:
	$(PYTHON) setup.py test

.PHONY: tests
tests: test

.PHONY: test-all
test-all:
	tox

.PHONY: coverage
coverage:
	coverage run --source $(PROJECT_NAME) setup.py test
	coverage report -m
	coverage html
	@echo "To view results type: htmlcov/index.html &"

.PHONY: docs
docs:
	rm -f docs/$(PROJECT_NAME)*.rst
	rm -f docs/modules.rst
	$(MAKE) -C docs clean
	sphinx-apidoc -o docs/ $(PROJECT_NAME)
	$(MAKE) -C docs html SPHINXBUILD='python3 $(shell which sphinx-build)'
	@echo "To view results type: firefox docs/_build/html/index.html &"

.PHONY: docs-pdf
docs-pdf:
	rm -f docs/$(PROJECT_NAME)*.rst
	rm -f docs/modules.rst
	$(MAKE) -C docs clean
	sphinx-apidoc -o docs/ $(PROJECT_NAME)
	$(MAKE) -C docs latexpdf SPHINXBUILD='python3 $(shell which sphinx-build)'
	@echo "To view results use something like: evince docs/_build/latex/$(PROJECT_NAME).pdf &"

.PHONY: docs-man
docs-man:
	rm -f docs/$(PROJECT_NAME)*.rst
	rm -f docs/modules.rst
	$(MAKE) -C docs clean
	sphinx-apidoc -o docs/ $(PROJECT_NAME)
	$(MAKE) -C docs man SPHINXBUILD='python3 $(shell which sphinx-build)'
	@echo "To view results use something like: man docs/_build/man/$(PROJECT_NAME).1 &"

.PHONY: docs-changelog
docs-changelog:
	gitchangelog

.PHONY: prepare-release
prepare-release: clean
	@echo "Current version: "$(PROJECT_VERSION)
	@while [ -z "$$NEW_VERSION" ]; do \
        read -r -p "Give new version: " NEW_VERSION;\
    done && \
    ( \
        printf 'Setting new version: %s \n\n' \
        	"$$NEW_VERSION " \
	) && sed -i -e "s/^\(VERSION\ =\ \)\('.*'\)\(\ *\)/\1'$$NEW_VERSION'/g" $(PROJECT_NAME)/__version__.py
	$(MAKE) docs-changelog
	@echo "Consider manually inspecting CHANGELOG.rst for possible improvements."

.PHONY: release
release: clean release-pip release-github

.PHONY: release-pip
release-pip:
	$(PYTHON) setup.py sdist bdist_wheel
	twine upload dist/$(PROJECT_NAME)-$(PROJECT_VERSION).tar.gz dist/$(PROJECT_NAME)-$(PROJECT_VERSION)-py2.py3-none-any.whl

.PHONY: release-github
release-github:
	git push . master:latest_release
	git tag -a v$(PROJECT_VERSION) -m "Version $(PROJECT_VERSION)"
	git push origin latest_release
	git push origin --tags

.PHONY: dist
dist: clean
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel
	ls -l dist

.PHONY: install
install: dist
	$(PIP) install --upgrade --no-deps --force-reinstall dist/$(PROJECT_NAME)-*.tar.gz

.PHONY: uninstall
uninstall:
	$(PIP) uninstall -y $(PROJECT_NAME)
