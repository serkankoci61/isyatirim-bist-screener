PYTHON ?= .venv/bin/python
OUT ?=
TICKERS ?=

.PHONY: setup run telegram clean

setup:
	uv venv .venv
	uv pip install --python .venv/bin/python -r requirements.txt

run:
	$(PYTHON) isyatirim_analiz.py $(if $(OUT),--output $(OUT),) $(if $(TICKERS),--tickers $(TICKERS),)

telegram:
	$(PYTHON) isyatirim_analiz.py --telegram $(if $(OUT),--output $(OUT),) $(if $(TICKERS),--tickers $(TICKERS),)

clean:
	rm -f isyatirim_analiz_raporu*.xlsx isyatirim_analiz_raporu*.json
