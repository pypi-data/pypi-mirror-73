# guietta

A tool for making simple Python GUIs

Guietta is a tool that makes simple GUIs *simple*:

```python
from guietta import _, Gui, Quit
gui = Gui(
	[ "Enter numbers:",  "__a__", "+", "__b__", ["Calculate"] ],
	[    "Result: -->", "result",   _,       _,             _ ],
	[                _,        _,   _,       _,          Quit ]
)

with gui.Calculate:
	gui.result = float(gui.a) + float(gui.b)

gui.run()
```
And here it is:

![Example GUI](http://guietta.com/_images/example.png)

Also featuring:
 * matplotlib and pyqtgraph integration, for easy event-driven plots
 * easily display columns of data in labels using lists and dicts
 * multiple windows
 * customizable behaviour in case of exceptions
 * queue-like mode (a la PySimpleGUI)
 * integrate any QT widget seamlessly, even your custom ones (as long as
   it derives from QWidget, it is OK)
 * easy background processing for long-running operations
 * ordinary QT signals/slots, accepting any Python callable, if you really
   want to use them

# Installation

 **pip install guietta**
 

If you use conda, please read our page on
[QT incompatibilities with conda](https://guietta.readthedocs.io/en/latest/qt_conda.html).


# Documentation

https://guietta.readthedocs.io/en/latest/

# Tests

![](https://github.com/alfiopuglisi/guietta/workflows/lint_python/badge.svg)

