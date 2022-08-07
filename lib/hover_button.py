from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton

from app.func import Func
from app.info import Info


class HoverButton(QPushButton):
    def __init__(self, button_type: str, text: str = ""):
        super(HoverButton, self).__init__()
        self.button_type = button_type

        if Info.IS_RETINA_SCR_LINUX:
            self.iconSize = QSize(60, 60)
            self.textAlignmentCmd = 'text-align:left;'
        else:
            self.iconSize = QSize(30, 30)
            self.textAlignmentCmd = ''

        self.setIcon(Func.getImageObject(f"{self.button_type}.png", 1, self.iconSize))
        self.text = text
        if text:
            self.setText(text)
        self.setStyleSheet(f"""
        QPushButton{{
            border:none;
            {self.textAlignmentCmd}
            background:transparent;
        }}
        """)

    def enterEvent(self, QEvent):
        super(HoverButton, self).enterEvent(QEvent)
        self.setIcon(Func.getImageObject(f"{self.button_type}_pressed.png", 1, self.iconSize))
        if self.text:
            # self.setText(self.text)
            self.setStyleSheet("""
                            QPushButton{
                                border:none;
                                color:rgb(59,120,181);
                                text-align:center;
                                background:transparent;
                            }
                            """)

    def leaveEvent(self, QEvent):
        super(HoverButton, self).leaveEvent(QEvent)
        self.setIcon(Func.getImageObject(f"{self.button_type}.png", 1, self.iconSize))
        if self.text:
            # self.setText(self.text)
            self.setStyleSheet(f"""
                            QPushButton{{
                                border:none;
                                background:transparent;
                            }}
                            """)
