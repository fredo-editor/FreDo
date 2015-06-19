UIC = pyuic4
WIDGETS = main_window.py

%.py: %.ui
	$(UIC) -o $@ $^

all: $(WIDGETS)
