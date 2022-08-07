import os

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QPushButton, QFileDialog, QGridLayout, QLabel

from app.deviceSystem.describer.basis import Shower
from app.func import Func
from app.info import Info
from lib import ColComboBox


class Screen(Shower):
    def __init__(self, parent=None):
        super(Screen, self).__init__(parent=parent)
        self.device_index = QLineEdit()
        self.device_index.setToolTip("Screen index as returned by Screen('screens') in MATLAB")
        self.device_index.textEdited.connect(self.showAddressTip)
        self.bg_color = ColComboBox()
        self.mu_sample = QLineEdit()
        self.mu_sample.setToolTip("Number of samples are computed and combined into a single output pixel. \n A value greater than zero enables automatic hardware anti-aliasing of the display.")
        self.resolution = QLineEdit("auto")
        self.resolution.setValidator(QRegExpValidator(QRegExp(r"\d+x\d+|auto")))
        self.resolution.setToolTip("WidthxHeight (e.g., 1920x1080, \"x\" is the letter in the alphabet)")
        self.refresh_rate = QLineEdit("auto")
        self.refresh_rate.setToolTip("Refresh rate of the monitor (e.g., 60)")
        self.physic_size = QLineEdit()
        self.physic_size.setToolTip("Physical size of the monitor in mm (e.g., 400x300, \"x\" is the letter in the alphabet)")
        self.viewing_distance = QLineEdit()
        self.viewing_distance.setToolTip("Viewing distance in mm. For Eyetracker only (e.g., 570)")

        self.file_name = QLineEdit("")
        self.file_name.setToolTip("either a *.txt or *.mat file")

        self.open_bt = QPushButton("Find Color Look-up Table File")
        self.open_bt.clicked.connect(self.openFile)


        self.device_index.setValidator(QRegExpValidator(QRegExp(r"\d+")))
        self.mu_sample.setValidator(QRegExpValidator(QRegExp(r"\d+")))
        self.physic_size.setValidator(QRegExpValidator(QRegExp(r"\d+\.?\d+|\d+\.?\d+[xX,]\d+\.?\d+|NaN|auto")))
        self.viewing_distance.setValidator(QRegExpValidator(QRegExp(r"\d+\.?\d+|\d+\.?\d+,\d+\.?\d+|NaN")))

        # self.index_tip.setHtml("About the \"x\" in Resolution and Physic size:"
        #                        "<br><br><b>Device index</b>: Screen index as returned by Screen('screens') in MATLAB."
        #                        "<br><br><b>Resolution</b>: WidthxHeight e.g., 1024x768"
        #                        "<br><br><b>physic size</b> (for Eyetracker Only) mm: WdithxHeight, e.g., 500x400"
        #                        "<br><br><b>Viewing distance</b> (for Eyetracker Only) mm: e.g., 570"
        #                        "<br><br><b>!x is the char before y</b>")

        self.setUI()

    def setUI(self):
        layout1 = QGridLayout()

        l0 = QLabel("Color Look-up Table File:")
        l1 = QLabel("Device Type:")
        l2 = QLabel("Device Name:")
        l3 = QLabel("Device Index:")
        l4 = QLabel("Background Color:")
        l5 = QLabel("Multiple Sampling:")
        l6 = QLabel("Resolution:")
        l7 = QLabel("Refresh Rate (Hz):")
        l8 = QLabel("Physical Size (mm):")
        l9 = QLabel("Viewing Distance (mm):")

        l0.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        l1.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        l8.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        l9.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout1.addWidget(l1, 0, 0, 1, 1)
        layout1.addWidget(self.device_type, 0, 1, 1, 5)
        layout1.addWidget(l2, 1, 0, 1, 1)
        layout1.addWidget(self.device_name, 1, 1, 1, 5)
        layout1.addWidget(l3, 2, 0, 1, 1)
        layout1.addWidget(self.device_index, 2, 1, 1, 5)
        layout1.addWidget(l4, 3, 0, 1, 1)
        layout1.addWidget(self.bg_color, 3, 1, 1, 5)
        layout1.addWidget(l5, 4, 0, 1, 1)
        layout1.addWidget(self.mu_sample, 4, 1, 1, 5)
        layout1.addWidget(l6, 5, 0, 1, 1)
        layout1.addWidget(self.resolution, 5, 1, 1, 5)
        layout1.addWidget(l7, 6, 0, 1, 1)
        layout1.addWidget(self.refresh_rate, 6, 1, 1, 5)
        layout1.addWidget(l8, 7, 0, 1, 1)
        layout1.addWidget(self.physic_size, 7, 1, 1, 5)
        layout1.addWidget(l9, 8, 0, 1, 1)
        layout1.addWidget(self.viewing_distance, 8, 1, 1, 5)

        layout1.addWidget(l0, 9, 0, 1, 1)
        layout1.addWidget(self.file_name, 9, 1, 1, 5)
        layout1.addWidget(self.open_bt, 10, 0, 1, 6)

        # layout = QFormLayout()
        # layout.setLabelAlignment(Qt.AlignLeft)
        # layout.addRow("Device Type:", self.device_type)
        # layout.addRow("Device Name:", self.device_name)
        # layout.addRow("Device Index:", self.device_index)
        # layout.addRow("Background Color:", self.bg_color)
        # layout.addRow("Multiple Sampling:", self.mu_sample)
        # layout.addRow("Resolution:", self.resolution)
        # layout.addRow("Refresh Rate (Hz):", self.refresh_rate)
        # layout.addRow("Physical Size (mm):", self.physic_size)
        # layout.addRow("Viewing Distance (mm):", self.viewing_distance)

        vLayout = QVBoxLayout()
        vLayout.addLayout(layout1)
        vLayout.addWidget(self.port_tip)
        vLayout.addWidget(self.index_tip)

        self.setLayout(vLayout)


    def openFile(self):
        options = QFileDialog.Options()

        if self.file_name.text():
            file_directory = self.file_name.text()
        else:
            file_directory = Info.FILE_DIRECTORY
            if not file_directory:
                file_directory = os.path.dirname(os.path.abspath(__file__))

        file_name, _ = QFileDialog.getOpenFileName(self, "Find the Color Look-up Table File", file_directory,
                                                   "Image File (*.mat;*.txt)", options=options)
        file_name = Func.getRelativeFilePath(file_name)
        if file_name:
            self.file_name.setText(file_name)

    def describe(self, info: dict):
        super().describe(info)
        self.device_index.setText(info.get("Device Index", "0"))
        self.bg_color.setCurrentText(info.get("Back Color", "255,255,255"))
        self.mu_sample.setText(info.get("Multi Sample", ""))
        self.resolution.setText(info.get("Resolution", "auto"))
        self.refresh_rate.setText(info.get("Refresh Rate", "auto"))
        self.physic_size.setText(info.get("Physic Size", ""))
        self.viewing_distance.setText(info.get("Viewing Distance", ""))
        self.file_name.setText(info.get("Gamma Filename", ""))

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Device Index": self.device_index.text(),
            "Back Color": self.bg_color.getRGB(),
            "Multi Sample": self.mu_sample.text(),
            "Resolution": self.resolution.text(),
            "Refresh Rate": self.refresh_rate.text(),
            "Physic Size": self.physic_size.text(),
            "Viewing Distance": self.viewing_distance.text(),
            "Gamma Filename": self.file_name.text(),
        }
        return properties