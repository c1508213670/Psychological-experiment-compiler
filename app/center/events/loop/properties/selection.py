from PyQt5.QtWidgets import QWidget, QComboBox, QGroupBox, QHBoxLayout, QFormLayout, QLabel


class Selection(QWidget):
    def __init__(self, parent=None):
        super(Selection, self).__init__(parent)

        self.order = QGroupBox("Order")

        self.order_combo = QComboBox(self.order)
        self.order_combo.addItem("Sequential")
        self.order_combo.addItem("Random without Replacement")
        self.order_combo.addItem("Random with Replacement")
        self.order_combo.addItem("Counter Balance")

        # self.no_repeat_after = QComboBox(self.order)
        # self.no_repeat_after.addItem("N/A")
        # self.no_repeat_after.setEnabled(False)

        form_1 = QFormLayout(self.order)

        form_1.addRow(self.order_combo)
        # form_1.addRow(QLabel(""))
        # form_1.addRow(QLabel(""))
        # form_1.addRow(QLabel(""))
        # form_1.addRow(QLabel("No Repeat After"))
        # form_1.addRow(self.no_repeat_after)

        self.order.setLayout(form_1)

        self.order_by = QGroupBox("Order By")

        self.order_by_combo = QComboBox(self.order_by)
        self.order_by_combo.addItem("N/A")
        self.order_by_combo.setEnabled(False)

        form_2 = QFormLayout(self.order_by)
        form_2.addRow(self.order_by_combo)

        self.order_by.setLayout(form_2)

        h_box = QHBoxLayout(self)

        h_box.addWidget(self.order)
        h_box.addWidget(self.order_by)

        self.setLayout(h_box)
        self.setMinimumWidth(500)

        # 信号
        self.order_combo.currentIndexChanged.connect(self.setComboEnable)

    def setComboEnable(self, index):
        if index == 0 or index == 2:
            # self.no_repeat_after.setEnabled(False)
            # self.no_repeat_after.clear()
            # self.no_repeat_after.addItem("N/A")
            self.order_by_combo.setEnabled(False)
            self.order_by_combo.clear()
            self.order_by_combo.addItem("N/A")
        if index == 1:
            # self.no_repeat_after.setEnabled(True)
            # self.no_repeat_after.clear()
            # self.no_repeat_after.addItem("N/A")
            # self.no_repeat_after.addItem("Yes")
            # self.no_repeat_after.addItem("No")
            # self.no_repeat_after.setCurrentIndex(1)
            self.order_by_combo.setEnabled(False)
            self.order_by_combo.clear()
            self.order_by_combo.addItem("N/A")
        if index in (3, 4):
            # self.no_repeat_after.setEnabled(False)
            # self.no_repeat_after.clear()
            # self.no_repeat_after.addItem("N/A")
            self.order_by_combo.setEnabled(True)
            self.order_by_combo.clear()
            self.order_by_combo.addItem("N/A")
            self.order_by_combo.addItem("Subject")
            self.order_by_combo.addItem("Session")
            self.order_by_combo.addItem("Run")
            self.order_by_combo.setCurrentIndex(1)
