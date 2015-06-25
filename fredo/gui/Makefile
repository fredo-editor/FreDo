UIC = pyside-uic
WIDGETS = main_window.py brush_dialog.py

%.py: %.ui
	$(UIC) -o $@ $^

all: $(WIDGETS)
