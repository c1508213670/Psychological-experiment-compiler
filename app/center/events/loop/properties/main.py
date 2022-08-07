from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QDialog, QTabWidget

from app.func import Func
from .selection import Selection


class Properties(QDialog):
    # 发送到cycle，告知发生properties变化 (null -> cycle)
    propertiesChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(Properties, self).__init__(parent)
        # title
        self.setWindowIcon(QIcon(Func.getImage("common/icon.png")))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Properties")
        # data
        self.properties = {"order_combo": 0, "no_repeat_after": 0, "order_by_combo": 0}
        # tabs
        self.tab = QTabWidget(self)
        self.selection = Selection()
        self.tab.addTab(self.selection, 'Selection')
        self.tab.setTabBarAutoHide(True)
        self.setButtons()
        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.tab, 7)
        layout.addWidget(self.btns, 1)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.resize(600, 420)

    def setButtons(self):
        self.btns = QWidget(self)
        self.ok_btn = QPushButton("OK")
        self.cancel_btn = QPushButton("Cancel")
        self.apply_btn = QPushButton("Apply")
        self.ok_btn.clicked.connect(self.ok)
        self.apply_btn.clicked.connect(self.apply)
        self.cancel_btn.clicked.connect(self.cancel)
        # layout
        layout = QHBoxLayout()
        layout.addStretch(10)
        layout.addWidget(self.ok_btn, 1)
        layout.addWidget(self.cancel_btn, 1)
        layout.addWidget(self.apply_btn, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        self.btns.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()

    def apply(self):
        self.properties['order_combo'] = self.selection.order_combo.currentIndex()
        # self.properties['no_repeat_after'] = self.selection.no_repeat_after.currentIndex()
        self.properties['order_by_combo'] = self.selection.order_by_combo.currentIndex()
        self.propertiesChanged.emit()

    def cancel(self):
        self.selection.order_combo.setCurrentIndex(self.properties['order_combo'])
        # self.selection.no_repeat_after.setCurrentIndex(self.properties['no_repeat_after'])
        self.selection.order_by_combo.setCurrentIndex(self.properties['order_by_combo'])
        self.close()

    def getProperties(self):
        properties = {}
        properties['order_combo'] = self.selection.order_combo.currentText()
        # properties['no_repeat_after'] = self.selection.no_repeat_after.currentText()
        properties['order_by_combo'] = self.selection.order_by_combo.currentText()
        return properties

    def setProperties(self, properties):
        self.selection.order_combo.setCurrentText(properties['order_combo'])
        # self.selection.no_repeat_after.setCurrentText(properties['no_repeat_after'])
        self.selection.order_by_combo.setCurrentText(properties['order_by_combo'])
