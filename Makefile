SHELL		:= /usr/bin/zsh
ACTIVATE_SRC 	:= ${HOME}/miniconda3/bin/activate
CONDA_ENV_NAME 	:= pytorch

create-dist :
	source ${ACTIVATE_SRC} ${CONDA_ENV_NAME} ; \
	python setup.py sdist bdist_wheel

upload : create-dist
	source ${ACTIVATE_SRC} ${CONDA_ENV_NAME} ; \
	python -m twine upload dist/*
