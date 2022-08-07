from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit, QComboBox

from app.deviceSystem.describer.basis import Shower
from app.info import Info


class Quest(Shower):
    def __init__(self, parent=None):
        super(Quest, self).__init__(parent)

        self.device_type = QLabel(Info.DEV_QUEST)
        self.device_name = QLabel("Unselected")
        self.guess_threshold = QLineEdit()
        self.guess_threshold.setToolTip("Used for starting test value")

        self.std_dev = QLineEdit()
        self.std_dev.setToolTip("Of estimated threshold")

        self.desired_proportion = QLineEdit()
        self.desired_proportion.setToolTip("Of correct responses")

        self.steepness = QLineEdit()
        self.steepness.setToolTip("Of the weibull psychometric function")

        self.proportion = QLineEdit()
        self.proportion.setToolTip("Of random responses at maximum stimulus intensity")

        self.chance_level = QLineEdit()

        self.method = QComboBox()
        self.method.addItems(("quantile", "mean", "mode"))
        self.method.setToolTip("Method to determine optimal test value")

        self.minimum = QLineEdit()
        self.maximum = QLineEdit()

        self.is_log10_transform = QComboBox()
        self.is_log10_transform.addItems(("Yes", "No"))

        self.grain = QLineEdit()
        self.grain.setToolTip("Step size of the internal table")

        self.range = QLineEdit()
        self.range.setToolTip("Intensity difference between the largest and smallest intensity")

        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Guess Threshold:", self.guess_threshold)
        layout.addRow("Standard Deviation:", self.std_dev)
        layout.addRow("Desired Proportion:", self.desired_proportion)
        layout.addRow("Steepness (β):", self.steepness)
        layout.addRow("Proportion (σ):", self.proportion)
        layout.addRow("Chance Level (γ):", self.chance_level)
        layout.addRow("Method:", self.method)
        layout.addRow("Minimum Test Value:", self.minimum)
        layout.addRow("Maximum Test Value:", self.maximum)
        layout.addRow("Is Log10 Transformed:", self.is_log10_transform)
        layout.addRow("Grain:", self.grain)
        layout.addRow("Range:", self.range)
        layout.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setLayout(layout)

    def describe(self, info: dict):
        super(Quest, self).describe(info)
        self.guess_threshold.setText(info.get("Guess Threshold", ""))
        self.std_dev.setText(info.get("Std. Dev.", ""))
        self.desired_proportion.setText(info.get("Desired Proportion", ""))
        self.steepness.setText(info.get("Steepness", ""))
        self.proportion.setText(info.get("Proportion", ""))
        self.chance_level.setText(info.get("Chance Level", ""))
        self.method.setCurrentText(info.get("Method", ""))
        self.minimum.setText(info.get("Minimum Test Value", ""))
        self.maximum.setText(info.get("Maximum Test Value", ""))
        self.is_log10_transform.setCurrentText(info.get("Is Log10 Transform", ""))
        self.grain.setText(info.get("Grain", ""))
        self.range.setText(info.get("Range", ""))

    def changeName(self, name: str):
        self.device_name.setText(name)

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Guess Threshold": self.guess_threshold.text(),
            "Std. Dev.": self.std_dev.text(),
            "Desired Proportion": self.desired_proportion.text(),
            "Steepness": self.steepness.text(),
            "Proportion": self.proportion.text(),
            "Chance Level": self.chance_level.text(),
            "Method": self.method.currentText(),
            "Minimum Test Value": self.minimum.text(),
            "Maximum Test Value": self.maximum.text(),
            "Is Log10 Transform": self.is_log10_transform.currentText(),
            "Grain": self.grain.text(),
            "Range": self.range.text()
        }
        return properties
