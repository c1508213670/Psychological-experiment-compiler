from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont


class AttributeHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(AttributeHighlighter, self).__init__(parent)

        self.__formats = self.initFormat()
        self.__rules = [QRegExp(r"\[[_\d\w\.]+\]"), QRegExp("@mean|@standard|@random")]

    @staticmethod
    def initFormat():
        attribute_format = QTextCharFormat()
        attribute_format.setFontFamily("courier")
        attribute_format.setFontPointSize(12)
        attribute_format.setForeground(QColor(Qt.darkBlue))
        attribute_format.setFontWeight(QFont.Bold)

        value_format = QTextCharFormat()
        value_format.setFontFamily("courier")
        value_format.setFontPointSize(12)
        value_format.setForeground(QColor(Qt.darkRed))
        value_format.setFontWeight(QFont.Bold)
        return attribute_format, value_format

    def updateRule(self, attributes: list):
        self.__rules[0] = QRegExp("|".join([r"\[%s\]" % i for i in attributes]))

    def highlightBlock(self, text):
        for rule, _format in zip(self.__rules, self.__formats):
            i = rule.indexIn(text)
            while i >= 0:
                length = rule.matchedLength()
                self.setFormat(i, length, _format)
                i = rule.indexIn(text, i + length)