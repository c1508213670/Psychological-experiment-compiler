import re

from PyQt5.QtGui import QBrush, QColor

from lib import TableWidgetItem


class AttributeItem(TableWidgetItem):
    def __init__(self, value: str):
        super(AttributeItem, self).__init__(value)

    def setText(self, text):
        """
        highlight var
        """
        super(AttributeItem, self).setText(text)
        if re.search(r"^\[.*?\]", text):
            self.setForeground(QBrush(QColor(0, 0, 255)))
        else:
            self.setForeground(QBrush(QColor(0, 0, 0)))

