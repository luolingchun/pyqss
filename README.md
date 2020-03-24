# pyqss

简体中文 | [English](README-en.md)

一个简约的QSS编辑器

## 安装

```shell
pip install pyqss
```

## 功能

- [x] 实时预览
- [x] 语法高亮
- [x] 自动补全
- [x] 国际化
- [x] 查找替换
- [x] 文件拖拽
- [ ] 自动吸附

## 使用方法

**快捷键：**

- `Ctrl+/`：注释
- `Ctrl+F`：查找替换

从pyqss导入Qss，将主界面注册到Qss中，即可使用：[示例](./examples/test.py)

```python
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from pyqss import Qss

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    # 注册主窗口
    qss = Qss(main_window)
    qss.show()

    app.exec_()
```
## 截图

![show](./screen/show.png)

![comment](./screen/comment.gif)

![find_replace](./screen/find_replace.gif)