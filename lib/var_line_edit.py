import re

from PyQt5.QtCore import QDataStream, QIODevice, QRegExp, pyqtSignal
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import QLineEdit

from app.info import Info
from .message_box import MessageBox

######################################
# created by yu
# this is a custom single line input widget
######################################


class VarLineEdit(QLineEdit):
    focusLost = pyqtSignal()

    Variable = r"^\[[_\d\.\w]+\]$"
    Float = r"^(-?\d+)(\.\d+)?$"
    Integer = r"^-?\d+$"
    Percentage = r"^(100|[1-9]?\d?)%$|0$"
    FloatPercentage = r"^(([1-9]{1}\d*)|(0{1}))(\.\d{0,2})?%$"

    def __init__(self, *__args):
        super(VarLineEdit, self).__init__(*__args)
        self.setAcceptDrops(True)

        self.textChanged.connect(self.matchVariable)
        self.focusLost.connect(self.checkValidity)

        self.is_variable = False
        self.valid_data: str = self.text()
        self.non_variable: str = self.text()
        self.reg_exp: str = ""

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat(Info.AttributesToWidget):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        data = e.mimeData().data(Info.AttributesToWidget)
        stream = QDataStream(data, QIODevice.ReadOnly)
        text = f"[{stream.readQString()}]"
        self.setText(text)

    def matchVariable(self, text: str):
        """
        match variable from the input text
        :param text:
        :type text: str
        :return: None
        :rtype:
        """
        if re.fullmatch(VarLineEdit.Variable, text):
            self.setStyleSheet("color: blue")
            self.setFont(QFont("Times", 9, QFont.Bold))
            self.is_variable = True
        else:
            self.setStyleSheet("color: black")
            self.setFont(QFont(Info.DEFAULT_FONT, 9, QFont.Normal))
            self.is_variable = False

    def setRegularExpress(self, reg_exp):
        if isinstance(reg_exp, str):
            self.reg_exp = f"{reg_exp}|{VarLineEdit.Variable}"
        else:
            self.reg_exp = f"{'|'.join(reg_exp)}|{VarLineEdit.Variable}"
        self.setValidator(QRegExpValidator(QRegExp(self.reg_exp), self))

    def focusOutEvent(self, e):
        self.focusLost.emit()
        QLineEdit.focusOutEvent(self, e)

    def checkValidity(self):
        text = self.text()
        if self.reg_exp != "" and re.fullmatch(self.reg_exp, text) is None:
            self.setText(self.valid_data)
            MessageBox.warning(self, "Invalid", f"Invalid Parameter '{text}'\nFormat must conform to\n{self.reg_exp}")
        else:
            self.valid_data = text
            if not self.is_variable:
                self.non_variable = text

    def getNonVariableData(self):
        """
        This function may unworkable when load a psy file
        Because  the non variable is not stored.
        Maybe we can change the variable format from [subName] to [subName]@100
        In the future.
        :return: the last non variable data
        :rtype: str
        """
        return self.non_variable

    def setColor(self, rgb):
        self.setStyleSheet("background: {}".format(rgb))
