# pyqss

English|[简体中文](README.md)

A simple QSS editor

## Install

```shell
pip install pyqss
```

## Features

- [x] Real-time Preview
- [x] Syntax highlighting
- [x] Automatic completion
- [x] i18n
- [ ] Find and replace
- [ ] File drag and drop
- [ ] Automatic adsorption

## Usage

Import QSS from pyqss and register the MainWindow into QSS, and enjoy it：[example](./examples/test.py)

```python
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from pyqss import Qss

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    # register  Mainwindow 
    qss = Qss(main_window)
    qss.show()

    app.exec_()
```
## Screenshot
- todo