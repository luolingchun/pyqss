# -*- coding: utf-8 -*-
# @Time    : 2019/3/22 13:22
# @Author  : llc
# @File    : setup.py

from setuptools import setup, find_packages
from pyqss import __version__

setup(
    name="pyqss",
    version=__version__,
    description='QSS编辑工具',
    author='llc',
    author_email='luolingchun.com@gmail.com',
    license='GPLv3',
    packages=find_packages(),
    data_files=[('pyqss/qss', ['pyqss/qss/default.qss'])],
    zip_safe=False,
    install_requires=['PyQt5','QScintilla']
)
