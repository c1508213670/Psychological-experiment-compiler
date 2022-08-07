from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from app.func import Func


class AddDeleteButton(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None, button_type='add'):
        super(AddDeleteButton, self).__init__(parent)
        self.button_type = button_type
        self.can_emit = True

        self.becomeEnabled()
        self.setFixedSize(20, 20)

    def mousePressEvent(self, QMouseEvent):
        if self.can_emit:
            self.clicked.emit()
            self.becomePressed()
        else:
            self.becomeDisabled()

    def mouseReleaseEvent(self, QMouseEvent):
        if self.can_emit:
            self.becomeEnabled()
        else:
            self.becomeDisabled()

    def setDisabled(self, disabled=False):
        if disabled:
            self.can_emit = False
            self.becomeDisabled()
        else:
            self.can_emit = True
            self.becomeEnabled()

    def becomeDisabled(self):
        if self.button_type == 'add':
            cPixmap = QPixmap(Func.getImage("operate/add_disabled.png"))
            # cPixmap.setTransformationMode(Qt.SmoothTransformation)

            self.setPixmap(cPixmap.scaled(20,20,Qt.KeepAspectRatio))
        elif self.button_type == 'delete':
            cPixmap = QPixmap(Func.getImage("operate/add_disabled.png"))
            # cPixmap.setTransformationMode(Qt.SmoothTransformation)
            # cPixmap.scaled(20, 20, Qt.KeepAspectRatio)
            self.setPixmap(cPixmap.scaled(20,20,Qt.KeepAspectRatio))

    def becomeEnabled(self):
        if self.button_type == 'add':
            cPixmap = QPixmap(Func.getImage("operate/add.png"))
            # cPixmap.setTransformationMode(Qt.SmoothTransformation)
            # cPixmap.scaled(20, 20, Qt.KeepAspectRatio)
            self.setPixmap(cPixmap.scaled(20,20,Qt.KeepAspectRatio))
        elif self.button_type == 'delete':
            cPixmap = QPixmap(Func.getImage("operate/delete.png"))
            # cPixmap.setTransformationMode(Qt.SmoothTransformation)
            # cPixmap.scaled(20, 20, Qt.KeepAspectRatio)
            self.setPixmap(cPixmap.scaled(20,20,Qt.KeepAspectRatio))

    def becomePressed(self):
        if self.button_type == 'add':
            cPixmap = QPixmap(Func.getImage("operate/add_press.png"))
            # cPixmap.setTransformationMode(Qt.SmoothTransformation)
            # cPixmap.scaled(20, 20, Qt.KeepAspectRatio)
            self.setPixmap(cPixmap.scaled(20,20,Qt.KeepAspectRatio))
        elif self.button_type == 'del':
            cPixmap = QPixmap(Func.getImage("operate/delete_press.png"))
            # cPixmap.setTransformationMode(Qt.SmoothTransformation)
            # cPixmap.scaled(20, 20, Qt.KeepAspectRatio)
            self.setPixmap(cPixmap.scaled(20,20,Qt.KeepAspectRatio))
