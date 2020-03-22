# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 14:02
# @Author  : llc
# @File    : keywords.py

WIDGET_LIST = ["QAbstractScrollArea", "QCheckBox", "QColumnView", "QComboBox", "QDateEdit", "QDateTimeEdit", "QDialog",
               "QDialogButtonBox", "QDockWidget", "QDoubleSpinBox", "QFrame", "QGroupBox", "QHeaderView", "QLabel",
               "QLineEdit", "QListView", "QListWidget", "QMainWindow", "QMenu", "QMenuBar", "QMessageBox",
               "QProgressBar", "QPushButton", "QRadioButton", "QScrollBar", "QSizeGrip", "QSlider", "QSpinBox",
               "QSplitter", "QStatusBar", "QTabBar", "QTabWidget", "QTableView", "QTableWidget", "QTextEdit",
               "QTimeEdit", "QToolBar", "QToolButton", "QToolBox", "QToolTip", "QTreeView", "QTreeWidget", "QWidget",
               "QsciScintilla", "QAbstractItemView"]

PROPERTY_LIST = ["alternate-background-color", "background", "background-color", "background-image",
                 "background-repeat", "background-position", "background-attachment", "background-clip",
                 "background-origin", "border", "border-top", "border-right", "border-bottom", "border-left",
                 "border-color", "border-top-color", "border-right-color", "border-bottom-color", "border-left-color",
                 "border-image", "border-radius", "border-top-left-radius", "border-top-right-radius",
                 "border-bottom-right-radius", "border-bottom-left-radius", "border-style", "border-top-style",
                 "border-right-style", "border-bottom-style", "border-left-style", "border-width", "border-top-width",
                 "border-right-width", "border-bottom-width", "border-left-width", "bottom", "button-layout", "color",
                 "dialogbuttonbox-buttons-have-icons", "font", "font-family", "font-size", "font-style", "font-weight",
                 "gridline-color", "height", "icon-size", "image", "image-position", "left",
                 "lineedit-password-character", "lineedit-password-mask-delay", "margin", "margin-top", "margin-right",
                 "margin-bottom", "margin-left", "max-height", "max-width", "messagebox-text-interaction-flags",
                 "min-height", "min-width", "opacity", "outline", "outline-color", "outline-offset", "outline-style",
                 "outline-radius", "outline-bottom-left-radius", "outline-bottom-right-radius",
                 "outline-top-left-radius", "outline-top-right-radius", "padding", "padding-top", "padding-right",
                 "padding-bottom", "padding-left", "paint-alternating-row-colors-for-empty-area", "position", "right",
                 "selection-background-color", "selection-color", "show-decoration-selected", "spacing",
                 "subcontrol-origin", "subcontrol-position", "titlebar-show-tooltips-on-buttons",
                 "widget-animation-duration", "text-align", "text-decoration", "top", "width"]

PROPERTY_TYPE_LIST = ['repeat-y', 'solid', 'repeat-x', 'window-text', 'bottom', 'dark', 'none', 'base',
                      'qradialgradient', 'bright-text', 'center', 'content', 'text', 'disabled', 'outset',
                      'qlineargradient', 'highlighted-text', 'link-visited', 'dot-dot-dash', 'ridge', 'margin',
                      'padding', 'top', 'highlight', 'border', 'button-text', 'selected', 'bold', 'stretch', 'left',
                      'groove', 'light', 'dotted', 'dot-dash', 'oblique', 'no-repeat', 'normal', 'alternate-base',
                      'double', 'qconicalgradient', 'right', 'shadow', 'button', 'window', 'repeat', 'scroll', 'italic',
                      'fixed', 'dashed', 'link', 'inset', 'midlight', 'active', 'mid']

ICON_LIST = ["backward-icon", "cd-icon", "computer-icon", "desktop-icon", "dialog-apply-icon", "dialog-cancel-icon",
             "dialog-close-icon", "dialog-discard-icon", "dialog-help-icon", "dialog-no-icon", "dialog-ok-icon",
             "dialog-open-icon", "dialog-reset-icon", "dialog-save-icon", "dialog-yes-icon", "directory-closed-icon",
             "directory-icon", "directory-link-icon", "directory-open-icon", "dockwidget-close-icon", "downarrow-icon",
             "dvd-icon", "file-icon", "file-link-icon", "filedialog-contentsview-icon", "filedialog-detailedview-icon",
             "filedialog-end-icon", "filedialog-infoview-icon", "filedialog-listview-icon",
             "filedialog-new-directory-icon", "filedialog-parent-directory-icon", "filedialog-start-icon",
             "floppy-icon", "forward-icon", "harddisk-icon", "home-icon", "leftarrow-icon", "messagebox-critical-icon",
             "messagebox-information-icon", "messagebox-question-icon", "messagebox-warning-icon", "network-icon",
             "rightarrow-icon", "titlebar-contexthelp-icon", "titlebar-maximize-icon", "titlebar-menu-icon",
             "titlebar-minimize-icon", "titlebar-normal-icon", "titlebar-shade-icon", "titlebar-unshade-icon",
             "trash-icon", "uparrow-icon"]

COLOR_LIST = ["aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque", "black", "blanchedalmond",
              "blue", "blueviolet", "brown", "burlywood", "cadetblue", "chartreuse", "chocolate", "coral",
              "cornflowerblue", "cornsilk", "crimson", "cyan", "darkblue", "darkcyan", "darkgoldenrod", "darkgray",
              "darkgreen", "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred",
              "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkturquoise", "darkviolet", "deeppink",
              "deepskyblue", "dimgray", "dodgerblue", "feldspar", "firebrick", "floralwhite", "forestgreen", "fuchsia",
              "gainsboro", "ghostwhite", "gold", "goldenrod", "gray", "green", "greenyellow", "honeydew", "hotpink",
              "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon",
              "lightblue", "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgrey", "lightgreen", "lightpink",
              "lightsalmon", "lightseagreen", "lightskyblue", "lightslateblue", "lightslategray", "lightsteelblue",
              "lightyellow", "lime", "limegreen", "linen", "magenta", "maroon", "mediumaquamarine", "mediumblue",
              "mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumspringgreen",
              "mediumturquoise", "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin", "navajowhite",
              "navy", "oldlace", "olive", "olivedrab", "orange", "orangered", "orchid", "palegoldenrod", "palegreen",
              "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru", "pink", "plum", "powderblue",
              "purple", "red", "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen", "seashell",
              "sienna", "silver", "skyblue", "slateblue", "slategray", "snow", "springgreen", "steelblue", "tan",
              "teal", "thistle", "tomato", "turquoise", "violet", "violetred", "wheat", "white", "whitesmoke", "yellow",
              "yellowgreen", "rgb", "rgba", "hsv", "hsva", "hsl", "hsla"]

LENGTH_LIST = ["px", "pt", "em", "ex"]

PSEUDO_STATE_LIST = ["_opened", "adjoins-item", "alternate", "bottom", "checked", "closable", "closed", "default",
                     "disabled", "editable", "edit-focus", "enabled", "exclusive", "first", "flat", "floatable",
                     "focus", "has-children", "has-siblings", "horizontal", "hover", "indeterminate", "last", "left",
                     "maximized", "middle", "minimized", "movable", "no-frame", "non-exclusive", "off", "on",
                     "only-one", "open", "next-selected", "pressed", "previous-selected", "read-only", "right",
                     "selected", "top", "unchecked", "vertical", "window"]

SUB_CONTROL_LIST = ["add-line", "add-page", "branch", "chunk", "close-button", "corner", "down-arrow",
                    "down-button", "drop-down", "float-button", "groove", "indicator", "handle", "icon",
                    "item", "left-arrow", "left-corner", "menu-arrow", "menu-button", "menu-indicator",
                    "right-arrow", "pane", "right-corner", "scroller", "section", "separator", "sub-line",
                    "sub-page", "tab", "tab-bar", "tear", "tearoff", "text", "title", "up-arrow",
                    "up-button"]

API_LIST = WIDGET_LIST + PROPERTY_LIST + PROPERTY_TYPE_LIST + PSEUDO_STATE_LIST + COLOR_LIST + SUB_CONTROL_LIST \
           + ICON_LIST + LENGTH_LIST
