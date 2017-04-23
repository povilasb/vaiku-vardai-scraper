python ?= python3
virtualenv_dir := pyenv
pip := $(virtualenv_dir)/bin/pip
py_requirements ?= requirements/prod.txt requirements/dev.txt
pytest := $(virtualenv_dir)/bin/py.test


$(virtualenv_dir): $(py_requirements)
	$(python) -m venv $@
	for r in $^ ; do \
		$(pip) install -r $$r ; \
	done
