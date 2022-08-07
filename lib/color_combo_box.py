from PyQt5.QtCore import Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QColor, QIcon, QRegExpValidator, QFont
from PyQt5.QtWidgets import QComboBox, QColorDialog

from app.func import Func
from app.info import Info
from .var_combo_box import VarComboBox


class ColComboBox(VarComboBox):
    colorChanged = pyqtSignal(str)

    color_map: dict = {
        "White": "255,255,255",
        "Gray": "128,128,128",
        "Black": "0,0,0",
        "Red": "255,0,0",
        "Orange": "255,165,0",
        "Yellow": "255,255,0",
        "Green": "0,255,0",
        "Blue": "0,0,255",
        "Purple": "128,0,128",
        "Transparent": "0,0,0,0"
    }
    default_color = ("White", "Gray", "Black",
                     "Red", "Orange", "Yellow",
                     "Green", "Blue", "Purple")

    def __init__(self, widget=None):
        super(ColComboBox, self).__init__(True, widget)
        self.setEditable(True)
        self.is_valid: int = 1
        self.default_color = ("White", "Gray", "Black", "Red",
                              "Orange", "Yellow", "Green", "Blue", "Purple")
        self.init()

        self.setStyleSheet("background: {}".format(self.getRGB()))
        self.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        # 支持输入255,255,255及#ffffff格式rgb
        valid_rgb = QRegExp(
            r"((2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?),){2}((2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?))|#[0-9A-Fa-f]{6}|"
            r"White|Gray|Black|Red|Orange|Yellow|Green|Blue|Purple|\[[\w_\.]+\]")
        self.setValidator(QRegExpValidator(valid_rgb, self))
        self.setInsertPolicy(QComboBox.NoInsert)

        self.rgb = "255,255,255"

    # 添加默认颜色，白灰黑、红橙黄绿蓝紫
    def init(self):
        for i, color_name in enumerate(ColComboBox.default_color):
            color = QColor(color_name)
            self.insertItem(i, color_name)
            self.setItemData(i, color, Qt.DecorationRole)
        self.insertItem(0, "More...", Qt.DecorationRole)
        self.setItemIcon(0, QIcon(Func.getImage("operate/more_color.png")))

    def addTransparent(self):
        color_name = "Transparent"
        color = QColor(color_name)
        self.insertItem(1, color_name)
        self.setItemData(1, color, Qt.DecorationRole)
        self.setCurrentIndex(1)

    def searchVariable(self, current_text: str):
        if current_text:
            if current_text.startswith("["):
                self.setStyleSheet("color: blue")
                self.setFont(QFont("Times", 9, QFont.Bold))
                self.is_valid = 2
            else:
                self.setStyleSheet("color: black")
                self.setFont(QFont(Info.DEFAULT_FONT, 9, QFont.Normal))
                # 取色板
                if current_text == "More...":
                    self.setStyleSheet("background: white;")
                    color_rgb = QColorDialog.getColor(Qt.white, self)
                    # 选了颜色
                    if color_rgb.isValid():
                        color_name = color_rgb.name()
                        color_name_ = f"{int(color_name[1:3], 16)},{int(color_name[3:5], 16)},{int(color_name[5:], 16)}"
                        self.setStyleSheet("background: {}".format(color_name))
                        self.setCurrentText(color_name_)
                    # 未选颜色
                    else:
                        self.setCurrentIndex(1)
                    self.is_valid = 1
                # 255,255,255格式rgb
                elif current_text[0].isdigit():
                    color_rgb = current_text.split(",")
                    if len(color_rgb) >= 3 and color_rgb[2] != "":
                        self.setStyleSheet("background-color: rgb({});".format(current_text))
                        # 添加到下拉菜单
                        if self.findText(current_text, Qt.MatchExactly) == -1:
                            color = QColor(int(color_rgb[0]), int(
                                color_rgb[1]), int(color_rgb[2]))
                            self.insertItem(1, current_text)
                            self.setItemData(1, color, Qt.DecorationRole)
                            self.setCurrentIndex(1)
                        self.is_valid = 1
                    else:
                        self.is_valid = 0
                        self.setStyleSheet("background: white")
                # #ffffff格式rgb
                elif current_text[0] == "#" and len(current_text) == 7:
                    if self.findText(current_text) == -1:
                        color = QColor(current_text)
                        self.insertItem(1, current_text)
                        self.setItemData(1, color, Qt.DecorationRole)
                        self.setCurrentIndex(1)
                    self.setStyleSheet("background: {}".format(current_text))
                    self.is_valid = 1
                elif current_text in ColComboBox.default_color:
                    self.is_valid = 1
                    self.setStyleSheet("background: rgb({})".format(self.color_map.get(current_text)))
                elif current_text == "transparent":
                    self.is_valid = 1
                    self.setStyleSheet("background: transparent")
                else:
                    self.is_valid = 0
                    self.setStyleSheet("background: white")
        else:
            self.is_valid = 0
            self.setStyleSheet("background: white")

        if self.is_valid == 1:
            self.colorChanged.emit(self.getRGB())

    # 重写下拉菜单展开
    def showPopup(self):
        self.setStyleSheet("background: white;")
        QComboBox.showPopup(self)

    # 重写下拉菜单收起
    def hidePopup(self):
        color = self.currentText()
        if self.is_valid == 1:
            if ',' in color:
                self.setStyleSheet("background: rgb({})".format(color))
            else:
                self.setStyleSheet("background: {};".format(color))
        elif self.is_valid == 2:
            self.setStyleSheet("color: blue")
            self.setFont(QFont("Times", 9, QFont.Bold))
        else:
            self.setStyleSheet("background: white;")
        QComboBox.hidePopup(self)

    # def focusOutEvent(self, e):
    #     if not self.is_valid:
    #         self.setStyleSheet("background: white;")
    #         self.setCurrentText("white")
    #         MessageBox.warning(
    #             self, "Warning", "Invalid Color!", MessageBox.Ok)
    #     else:
    #         pass
    #     QComboBox.focusOutEvent(self, e)

    def setCurrentText(self, text: str) -> None:
        for k, v in self.color_map.items():
            if text == v:
                text = k
                break
        return QComboBox.setCurrentText(self, text)

    def getColor(self) -> QColor or None:
        """
        返回当前颜色QColor
        :return:
        """
        index = self.findText(self.currentText())
        if index != -1:
            color = self.itemData(index, Qt.DecorationRole)
            if color:
                if isinstance(color, QColor):
                    return QColor(color)
            else:
                return QColor(255, 255, 255)
        else:
            return QColor(255, 255, 255)
        r, g, b = [int(x) for x in self.rgb.split(",")]
        return QColor(r, g, b)

    def getRGB(self) -> str:
        color_name = self.currentText()
        if color_name.startswith("["):
            pass
        elif color_name.startswith("#"):
            color_name = f"{int(color_name[1:3], 16)},{int(color_name[3:5], 16)},{int(color_name[5:], 16)}"

        self.rgb = self.color_map.get(color_name, color_name)
        return self.rgb
