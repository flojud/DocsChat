VENV_NAME = venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip


.PHONY: clean install run

clean:
	rm -rf $(VENV_NAME)
	rm -rf __pycache__
	rm -rf vector_db/
	rm -rf dist/

install:
	python3 -m venv $(VENV_NAME)
	 . $(VENV_NAME)/bin/activate

run:
	streamlit run src/docschat/app.py
release:
	bump2version minor
	$(PYTHON) -m build