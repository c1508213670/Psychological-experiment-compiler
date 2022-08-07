import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QGridLayout, QVBoxLayout, QLineEdit, QComboBox, QApplication, \
    QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy

from app.func import Func


class subjectInfo(QWidget):
    def __init__(self, parent = None):
        super(subjectInfo, self).__init__(parent)
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        # app.setStyle('Fusion')
        self.setMinimumSize(420, 360)
        self.setMaximumSize(420, 360)

        self._name = QLineEdit()
        self._name.setText("Yang Zhang")
        self._name.setAlignment(Qt.AlignCenter)

        self._age = QLineEdit()
        self._age.setText("38")
        self._age.setAlignment(Qt.AlignCenter)

        self._gender = QComboBox()
        self._gender.setEditable(False)
        self._gender.addItems(("male", "female"))

        self._handedness = QComboBox()
        self._handedness.setEditable(False)
        self._handedness.addItems(("left", "right"))

        self._subNum = QLineEdit()
        self._subNum.setText("1")
        self._subNum.setAlignment(Qt.AlignCenter)

        self._runNum = QLineEdit()
        self._runNum.setText("1")
        self._runNum.setAlignment(Qt.AlignCenter)

        self._sessionNum = QLineEdit()
        self._sessionNum.setText("1")
        self._sessionNum.setAlignment(Qt.AlignCenter)

        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Quit")

        self.setUI()

    def setUI(self):
        self.setWindowTitle("Subject Information")
        l00 = QLabel("Name:")
        l10 = QLabel("Age:")

        l20 = QLabel("Gender:")
        l30 = QLabel("Handedness:")

        l41 = QLabel("Subject:")
        l42 = QLabel("Run:")
        l43 = QLabel("Session:")

        designer = QLabel("Designed By Yang Zhang at Soochow University")

        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l41.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l42.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l43.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        designer.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)




        # group_subInfo = QGroupBox("")
        # # group_subInfo.setFlat(True)
        # group_subInfo.setStyleSheet(f"""
        # QGroupBox {{
        # border: 0px solid gray;
        # border-radius: 5px;
        # margin-top: 1ex; /* leave space at the top for the title */
        # }}
        #
        # QGroupBox::title {{
        #     subcontrol-origin: margin;
        #     subcontrol-position: top center; /* position at the top center */
        #     padding: 0 3px;
        # }}
        #
        # """)



        layout1 = QGridLayout()
        layout1.setVerticalSpacing(30)

        strCol = 1
        strIconCol=2

        iRow = 0
        layout1.addItem(QSpacerItem(120,20, QSizePolicy.Maximum, QSizePolicy.Maximum),iRow,0)
        iRow += 1

        layout1.addWidget(l00, iRow, strCol, 1, 1)
        layout1.addWidget(self._name, iRow, strIconCol, 1, 1)
        # layout1.setRowStretch(iRow,1)
        iRow += 1

        layout1.addWidget(l10, iRow, strCol,1,1)
        layout1.addWidget(self._age, iRow, strIconCol,1,1)
        # layout1.setRowStretch(iRow,1)
        iRow += 1

        layout1.addWidget(l20, iRow, strCol,1,1)
        layout1.addWidget(self._gender, iRow, strIconCol,1,1)
        # layout1.setRowStretch(1,1)
        iRow += 1

        layout1.addWidget(l30, iRow, strCol,1,1)
        layout1.addWidget(self._handedness, iRow, strIconCol,1,1)
        layout1.addItem(QSpacerItem(120,20, QSizePolicy.Maximum, QSizePolicy.Maximum),iRow,strIconCol+1)
        iRow += 1


        # group_subInfo.setLayout(layout1)

        group_nums = QGroupBox('Numbers')
        group_nums.setFlat(True)

        layout_nums = QHBoxLayout()
        layout_nums.addWidget(l41,1)
        layout_nums.addWidget(self._subNum,1)
        layout_nums.addWidget(l42,1)
        layout_nums.addWidget(self._runNum,1)
        layout_nums.addWidget(l43,1)
        layout_nums.addWidget(self._sessionNum,1)

        group_nums.setLayout(layout_nums)



        deisgner_layout = QVBoxLayout()
        deisgner_layout.addWidget(designer)

        buttons_layout = QHBoxLayout()
        # buttons_layout.addStretch(10)
        buttons_layout.addWidget(self.ok_bt, 1)
        # buttons_layout.addStretch(3)
        # buttons_layout.addWidget(self.cancel_bt, 1)
        buttons_layout.addStretch(3)
        buttons_layout.addWidget(self.apply_bt, 1)
        # buttons_layout.setContentsMargins(0, 0, 0, 0)


        layout = QVBoxLayout()
        layout.addLayout(layout1)
        # layout.addWidget(group_subInfo)
        layout.addStretch(1)
        layout.addWidget(group_nums)
        layout.addStretch(1)
        layout.addLayout(buttons_layout)
        # layout.addStretch(1)
        layout.addLayout(deisgner_layout)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)


    sub_info = subjectInfo()
    sub_info.show()

    sys.exit(app.exec_())