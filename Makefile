HONY: \
    all \
	run \
	virtualenv \
	venv \
#SHELL:=/usr/bin/env bash
PYTHONPATH:=./venv/bin/python

all: virtualenv	run

clean:
	rm -rf venv

run:
	@${PYTHONPATH} mutual_exclusion.py 10 3 'pingpong'

virtualenv: requirements.txt | venv 
	@venv/bin/pip install -r requirements.txt

venv: venv/
	virtualenv venv
	venv/bin/pip install pip --upgrade
