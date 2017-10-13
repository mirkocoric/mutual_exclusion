PHONY: \
	all \
	run \
	virtualenv \
	venv \
#SHELL:=/usr/bin/env bash
PYTHONPATH:=./venv/bin/python

all: virtualenv	run

clean:
	rm -rf venv

lamport:
	@${PYTHONPATH} mutual_exclusion.py 3 3 'lamport' 0.01

run:
	@${PYTHONPATH} mutual_exclusion.py 2 3 'pingpong' 0.01

pingpong:
	@${PYTHONPATH} mutual_exclusion.py 2 3 'pingpong' 0.01

ricart_agrawala:
	@${PYTHONPATH} mutual_exclusion.py 3 3 'ricart_agrawala' 0.01

virtualenv: requirements.txt | venv
	@venv/bin/pip install -r requirements.txt

venv: venv/
	virtualenv venv
	venv/bin/pip install pip --upgrade
