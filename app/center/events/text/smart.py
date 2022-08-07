import re
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCompleter, QApplication, QTextEdit


"""
https://doc.qt.io/qt-5/qtwidgets-tools-customcompleter-example.html
https://stackoverflow.com/questions/58251763/how-to-construct-custom-auto-completion-completion-with-partial-matches-like-in
"""


class SmartCompleter(QCompleter):
    def __init__(self, words: list = list(), parent=None):
        super().__init__(words, parent)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseSensitive)

        self.setModelList(words)

        self.highlighted.connect(self.func)

        self.current_completion: str = ""

    def func(self, text):
        self.current_completion = text
        
    def setModelList(self, words: list):
        current_model = QStringListModel()
        if "@mean" not in words:
            words.extend(["@mean", "@mode", "@median"])
        current_model.setStringList(tuple(words))

        self.setModel(current_model)
        
    

class SmartTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.completer = SmartCompleter()
        self.completer.setWidget(self)
        self.completer.activated.connect(self.insertCompletion)
        self.textCursor().MoveMode(QTextCursor.MoveAnchor)
        self.setTextInteractionFlags(Qt.TextEditable|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

    def setModelList(self, words):
        self.completer.setModelList(words)
    #     self.setAcceptDrops(True)
    #
    # def dragEnterEvent(self, e):
    #     if e.mimeData().hasFormat(Info.AttributesToWidget):
    #         e.accept()
    #     else:
    #         e.ignore()
    #
    # def dropEvent(self, e: QDropEvent):
    #     data = e.mimeData().data(Info.AttributesToWidget)
    #     stream = QDataStream(data, QIODevice.ReadOnly)
    #     text = f"[{stream.readQString()}]"
    #     self.cursor().setPos(e.pos())
    #     self.insertPlainText(text)
    #
    def insertCompletion(self, completion):
        if completion == self.completer.completionPrefix():
            return
        text_cursor = self.textCursor()
        last_chars = len(completion) - len(self.completer.completionPrefix())
        text_cursor.insertText(completion[-last_chars:])
        self.setTextCursor(text_cursor)

    def textBeforeCursor(self):

        text_cursor = self.textCursor()
        cursor_position = text_cursor.position()

        text_cursor.select(QTextCursor.Document)

        selected_text = text_cursor.selectedText()

        ref_Pattern_txt = re.findall(r"\[[a-zA-z][a-zA-Z0-9_.]*$|\[$", selected_text[0:cursor_position])

        if ref_Pattern_txt:
            selected_text = ref_Pattern_txt[0]
        else:
            ref_Pattern_txt = re.findall(r"\[[a-zA-z][a-zA-Z0-9_.]+\]@[a-zA-Z]*$",selected_text[0:cursor_position])

            if ref_Pattern_txt:
                selected_text = ref_Pattern_txt[0]

                selected_text = re.findall(r"@[a-zA-Z]*$", selected_text)[0]
            else:
                selected_text = ""


        # if cursor_position > 2:
        #     selected_text = selected_text[(cursor_position - 2):cursor_position]
        #
        #     if "]@" == selected_text:
        #         selected_text = "@"
        #     elif "@" == selected_text[1]:
        #         selected_text = ""
        #     else:
        #         selected_text = selected_text[1]
        # elif cursor_position == 0:
        #     selected_text = ""
        # else:
        #     selected_text = selected_text[-1]
        # text_cursor.position() - text_cursor.block().position() # position in the current line
        # print(f"{cursor_position}:{selected_text}")

        text_cursor.clearSelection()

        # if "]@" in selected_text:
        #     return "@" + selected_text.split("@")[-1]
        return selected_text

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:

        if self.completer.popup().isVisible():
            key = e.key()
            if key in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab,Qt.Key_Backtab):
                e.ignore()
                return

        super().keyPressEvent(e)

        text_before_cursor = self.textBeforeCursor()

        # completionPrefix: This property holds the completion prefix used to provide completions.
        # currentCompletion : Returns the current completion string. This includes the completionPrefix.
        # When used alongside setCurrentRow(), it can be used to iterate through all the matches.

        if len(text_before_cursor)>0 and text_before_cursor != self.completer.currentCompletion():
        # if text_before_cursor != self.completer.completionPrefix():

            self.completer.setCompletionPrefix(text_before_cursor)
            self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

            cursor_rectangle = self.cursorRect()
            popup = self.completer.popup()

            cursor_rectangle.setWidth(popup.sizeHintForColumn(0) + popup.verticalScrollBar().sizeHint().width())

            # print(f"line 98: {cursor_rectangle}")
            self.completer.complete(cursor_rectangle)# popup it up!
        else:
            self.completer.popup().hide()


class SmartEditWidget(QWidget):
    def __init__(self):
        super().__init__()

        main_vertical_layout = QVBoxLayout()
        self.setLayout(main_vertical_layout)

        main_horizontal_layout = QHBoxLayout()
        main_vertical_layout.addLayout(main_horizontal_layout)

        text_edit = SmartTextEdit()
        main_horizontal_layout.addWidget(text_edit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    default_font = QFont()
    default_font.setPointSize(12)
    app.setFont(default_font)

    smart_edit_widget = SmartEditWidget()
    smart_edit_widget.showNormal()

    sys.exit(app.exec())
