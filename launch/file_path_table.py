import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QTextEdit, QApplication

from app.info import Info
from lib import TableWidget, HoverButton


class FilePath(QTextEdit):
    clicked = pyqtSignal()

    def __init__(self, file_path: str):
        # style
        super(FilePath, self).__init__()
        self.setStyleSheet("""
        QTextEdit{
            border:none;
            padding-left:10px;
            padding-top:5px;
        }
        QTextEdit:hover{
            border-radius:2px;
            border: 1px solid rgb(110, 110, 110);
        }
        """)
        self.file_path = file_path
        self.setToolTip(file_path)
        file_name = os.path.basename(file_path)
        self.setText(f"""<b style="color:rgb(31,31,31)">{file_name}</b>""")
        if len(file_path) > 45:
            file_path = file_path[:15] + "..." + file_path[-15:]

        if Info.IS_RETINA_SCR_LINUX:
            fontSize = 24
        else:
            fontSize = 12

        if os.path.exists(self.file_path):
            self.append(f"""<p style="color:rgb(157,157,157); font-size:{fontSize}px">{file_path}</p>""")
        else:
            self.append(f"""<p style="color:rgb(142,15,15); font-size:{fontSize}px">{file_path}</p>""")
        self.setReadOnly(True)
        self.setTextInteractionFlags(Qt.NoTextInteraction)

    def mousePressEvent(self, QMouseEvent):
        super(FilePath, self).mousePressEvent(QMouseEvent)
        self.clicked.emit()

    def enterEvent(self, QEvent):
        super(FilePath, self).enterEvent(QEvent)
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def leaveEvent(self, QEvent):
        super(FilePath, self).leaveEvent(QEvent)
        QApplication.restoreOverrideCursor()


class FilePathTable(TableWidget):
    """
    show some recent files
    """
    # emit file path
    filePathClicked = pyqtSignal(str)
    filePathDeleted = pyqtSignal(str)

    def __init__(self):
        super(FilePathTable, self).__init__()
        self.setShowGrid(False)
        self.setStyleSheet("border:none;border-right:1px solid rgb(236,236,236);background:white;")
        # hide headers
        self.horizontalHeader().setVisible(False)
        self.horizontalScrollBar().setVisible(False)
        self.verticalHeader().setVisible(False)

        # self.setMinimumHeight(40)
        # one column
        self.setColumnCount(2)

        if Info.IS_RETINA_SCR_LINUX:
            self.setColumnWidth(0, 596)
            self.setColumnWidth(1, 40)
        else:
            self.setColumnWidth(0, 298)
            self.setColumnWidth(1, 20)

    def addFilePath(self, index: int, file_path: str):
        """
        add file into table
        :param index:
        :param file_name:
        :param file_path:
        :return:
        """
        # add new row
        if index == -1:
            index = self.rowCount()
        self.insertRow(index)

        if Info.IS_RETINA_SCR_LINUX:
            self.setRowHeight(index, 100)
        else:
            self.setRowHeight(index, 50)

        # insert line edit into table
        file = FilePath(file_path)
        self.setCellWidget(index, 0, file)
        file.clicked.connect(lambda: self.filePathClicked.emit(file_path))
        # button
        delete_button = HoverButton("menu/close")
        self.setCellWidget(index, 1, delete_button)
        delete_button.clicked.connect(lambda checked: self.handleFileDeleted(file_path))

    def handleFileDeleted(self, file_path):
        """

        :param checked:
        :return:
        """
        self.filePathDeleted.emit(file_path)
        for row in range(self.rowCount()):
            if self.cellWidget(row, 0).file_path == file_path:
                self.removeRow(row)
                break
        if not self.rowCount():
            self.hide()
