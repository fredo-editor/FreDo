UIC = pyside-uic
RCC = pyside-rcc
WIDGETS = main_window.py brush_dialog.py res_rc.py

res_rc.py: res.qrc
	$(RCC) -o res_rc.py res.qrc

%.py: %.ui
	$(UIC) -o $@ $^

all: $(WIDGETS)
