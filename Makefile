VENV := .venv
PYTHON := $(VENV)\Scripts\python
PIP := $(VENV)\Scripts\pip

help:
	@echo "Usage:"
	@echo "  make setup      - Create venv and install dependencies"
	@echo "  make server     - Run unprotected server (port 5000)"
	@echo "  make protected  - Run protected server (port 5001)"
	@echo "  make attack     - Run attacker script"
	@echo "  make user       - Run legitimate user script"
	@echo "  make detector   - Run detector script"
	@echo "  make graph      - Run live traffic graph"
	@echo "  make clean      - Remove virtual environment"

setup:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

server:
	$(PYTHON) unprotected_server.py

protected:
	$(PYTHON) protected_server.py

attack:
	$(PYTHON) attacker.py

user:
	$(PYTHON) normal_user.py

detector:
	$(PYTHON) detector.py

graph:
	$(PYTHON) live_graph.py

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +