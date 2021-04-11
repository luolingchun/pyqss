# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 13:22
# @Author  : llc
# @File    : setup.py

from setuptools import setup

__version__ = '1.4.0'

long_description = """

A simple QSS editor

## Install

```shell
pip install pyqss
```

## Features

- Live preview
- Syntax highlighting
- Auto-completion
- i18n
- Find and replace
- File drag and drop
- Auto-attach

## Usage

Import QSS from pyqss and register the MainWindow into QSS, and enjoy it.

```python
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from pyqss import Qss

    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.show()
    # register  main_window
    qss = Qss(main_window)
    qss.show()

    app.exec_()
```
"""

setup(
    name="pyqss",
    version=__version__,
    url='https://github.com/luolingchun/pyqss',
    description='QSS Editor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='llc',
    author_email='luolingchun.com@gmail.com',
    license='GPLv3',
    packages=['pyqss', 'pyqss.sci', 'pyqss.ui', 'pyqss.widgets'],
    include_package_data=True,
    python_requires=">=3.6",
    zip_safe=False,
    platforms='any',
    install_requires=['PyQt5', 'QScintilla']
)
