# pyqss

English | [简体中文](README.md)

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
- [x] Find and replace
- [x] File drag and drop
- [ ] Automatic adsorption

## Usage

**shortcut keys**:

- `Ctrl+/`：comment
- `Ctrl+F`：find and replace

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
    qss = Qss(main_window, language='en')
    qss.show()

    app.exec_()
```
## Screenshot
![show](./screen/show.png)

![comment](./screen/comment.gif)

![find_replace](./screen/find_replace.gif)