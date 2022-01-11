# FreDo-Editor

![FreDo Program Window](http://fredo-editor.github.io/images/tutorial/view.jpg)

**Fre**quency **Do**main(FreDo) Editor is a free, open-source application for editing images in their frequency spectrum. It is intended to help visualize the 2D Fourier tranform and its effects. You can use it to observe how changes in the frequency domain affect the spatial domain. It can also be used to help in frequency domain filter design.

## Dependencies
Fredo-Editor uses [PySide](https://wiki.qt.io/PySide) for its GUI and
[NumPy](http://www.numpy.org/) for computation.

## Build Instructions

### Ubuntu
To run **FreDo** you need to have Python, numpy and PySide.
```bash
$ sudo apt-get install python python-numpy python-pyside pyside-tools
$ make run
```
