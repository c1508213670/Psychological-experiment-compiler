import datetime
import os
import re

from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QTextEdit, QAction

from app.info import Info
from lib import DockWidget


class Output(DockWidget):
    """
    This widget is used to output information about states of software.
    """

    def __init__(self):
        super(Output, self).__init__()
        # title
        self.setWindowTitle("Output")
        # main widget is a widget_name edit
        self.text_edit = MyQTextEdit()
        self.text_edit.setReadOnly(True)
        self.scroll_bar = self.text_edit.verticalScrollBar()
        # first str is work path of this software
        self.text_edit.setHtml(f"<b>{QDir().currentPath()}</b>")
        self.text_edit.append('<p style="font:5px;color:white">.</p>')
        self.setWidget(self.text_edit)

    def printOut(self, information: str, information_type: int = 0) -> None:
        """
        print information in its widget_name edit
        :param information:
        :param information_type: 0 none
                                 1 success
                                 2 fail
                                 3 compile error
        :return:
        """
        self.text_edit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        information = re.sub(r'\n', '<br>', information)
        # none
        if information_type == 0:
            self.text_edit.append(f"<p>{information}</p>")
        elif information_type == 1:
            self.text_edit.append(f'<b style="color:rgb(73,156,84)">[success]</b> {information}')
        elif information_type == 2:
            self.text_edit.append(f'<b style="color:rgb(199,84,80)">[fail]</b> {information}')
        elif information_type == 3:
            self.text_edit.append(f'<b style="color:rgb(255,84,80)">[error]</b> {information}')
            try:
                if Info.OS_TYPE ==0:
                    # only windows support
                    import winsound
                    winsound.MessageBeep(winsound.MB_ICONHAND)
                elif Info.OS_TYPE ==1:
                    # for mac ox
                    os.system('afplay /System/Library/Sounds/Funk.aiff')
                else:
                    # for linux at least for Unbuntu
                    os.system("paplay /usr/share/sounds/freedesktop/stereo/bell.oga")
            except:
                pass
        self.text_edit.append('<p style="font:5px;color:white">.</p>')
        # to the bottom
        self.scroll_bar.setSliderPosition(self.scroll_bar.maximum())


    def clear(self):
        """
        clear current_text
        :return:
        """
        self.text_edit.clear()
        self.text_edit.setHtml(f"<b>{QDir().currentPath()}</b>")
        self.text_edit.append('<p style="font:5px;color:white">.</p>')

class MyQTextEdit(QTextEdit):

    def __init__(self):
        super(MyQTextEdit, self).__init__()

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)

    def openMenu(self, e):
        menu = self.createStandardContextMenu()
        menu.addSeparator()

        clearAction = QAction("Clear", self)
        clearAction.triggered.connect(self.clearMe)

        menu.addAction(clearAction)
        menu.exec_(self.mapToGlobal(e))

    def clearMe(self):
        self.clear()
        self.setHtml(f"<b>{QDir().currentPath()}</b>")
        self.append('<p style="font:5px;color:white">.</p>')