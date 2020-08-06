SHELL		:= /usr/bin/zsh
ACTIVATE_SRC 	:= ${HOME}/miniconda3/bin/activate
CONDA_ENV_NAME 	:= pytorch

SELF		:= $(realpath $(dir $(firstword \
			${MAKEFILE_LIST})))
# PYTHON	:= source ${ACTIVATE_SRC} ${CONDA_ENV_NAME} ; python
PYTHON		:= python

create-dist :
	${PYTHON} setup.py sdist bdist_wheel

upload : create-dist
	${PYTHON} -m twine upload dist/*

.PHONY: try-example
try-example :
	cd $(realpath $(dir ${SELF})) ; \
	${PYTHON} -m ${notdir ${SELF}}.example \
	  --style2 alpha \
	  pop
