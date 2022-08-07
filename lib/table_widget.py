from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QItemDelegate, QStyle, QTableWidget


class NoDash(QItemDelegate):
    """
    clear table widget item' dash
    """

    def __init__(self):
        super(NoDash, self).__init__()

    def drawFocus(self, painter, option, rect):
        try:
            if option.state and QStyle.State_HasFocus:
                pen = QPen()
                pen.setWidth(0)
                painter.setPen(pen)
        except:
            pass


class TableWidget(QTableWidget):
    """

    """

    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)
        # clear dash
        self.setItemDelegate(NoDash())
        # set header's background color
        self.setStyleSheet("""
            QHeaderView::section {
                background:rgb(236,236,236);
                border: 1px solid rgb(189,189,189);
            }
            QHeaderView::section:hover {
                background:rgb(191,191,191);
            }
        """)
