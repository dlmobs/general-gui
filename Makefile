help:
	@echo "Usage:"
	@echo "  make install"

install:
	python -m venv venv
	. venv/Scripts/activate && python -m pip install -r requirements.txt && deactivate

