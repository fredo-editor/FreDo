UIC = pyside-uic
RCC = pyside-rcc
RCC_OPTS = -py3
UIC_OPTS = --from-imports
WIDGETS = main_window.py brush_dialog.py res_rc.py about_dialog.py new_image_dialog.py

res_rc.py: res.qrc
	$(RCC) $(RCC_OPTS) -o res_rc.py res.qrc

%.py: %.ui
	$(UIC) $(UIC_OPTS) -o $@ $^

all: $(WIDGETS)
