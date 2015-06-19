ALL_PY_FILES=$(shell find -name *.py)

all:gui

gui:
	make -C fredo/gui all

run: gui
	python -m fredo.editor.main
