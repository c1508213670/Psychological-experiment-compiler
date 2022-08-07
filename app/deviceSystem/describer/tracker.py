from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QCheckBox, QSpinBox, QGridLayout, QLineEdit, QComboBox

from app.deviceSystem.describer.basis import Shower
from app.info import Info


class Tracker(Shower):
    simple_info = {}

    def __init__(self, parent=None):
        super(Tracker, self).__init__(parent)

        self.device_name_tip = QLabel("Tracker Name:")
        self.device_name = QLabel("Unselected")

        self.tracker_type_tip = QLabel("Tracker Type:")
        self.tracker_type = QComboBox()
        # self.tracker_type.addItems(("Simple dummy", "Advanced dummy(mouse simulation)", "EyeLink", "SMI",
        #                             "EyeTribe", "OpenGaze", "Tobii", "Tobii-legacy", "Tobii Pro Glasses 2"))
        self.tracker_type.addItem("EyeLink")
        self.tracker_type.setItemData(0,
                                      "Currently, only Eyelink action is supported, because we only have an Eyelink 1000 for debug.\nEyetracker manufacturers are welcome to contact us for adding support.",
                                      Qt.ToolTipRole)
        self.tracker_type.currentIndexChanged.connect(self.typeChanged)

        self.calibrate_tracker = QCheckBox("Calibrate Tracker")
        self.calibration_beep = QCheckBox("Calibration Beep")

        # self.tracker_datafile_tip = QLabel("Eye Tracker Datafile:")
        self.tracker_datafile_tip = QLabel("Datafile:")
        self.tracker_datafile = QLineEdit("automatic")

        # self.velocity_threshold_tip = QLabel("Saccade Velocity Threshold:")
        self.velocity_threshold_tip = QLabel("Velocity:")
        self.velocity_threshold = QSpinBox()
        self.velocity_threshold.setSuffix("°/s")

        # self.acceleration_threshold_tip = QLabel("Saccade Acceleration Threshold:")
        self.acceleration_threshold_tip = QLabel("Acceleration:")
        self.acceleration_threshold = QSpinBox()
        self.acceleration_threshold.setSuffix("°/s/s")
        self.acceleration_threshold.setMaximum(99999)

        self.force_drift_correction = QCheckBox("Force Drift Correction")
        # self.force_drift_correction = QCheckBox("Force Drift Correction (For EyeLink 1000)")

        self.pupil_size_mode_tip = QLabel("Pupil Size Mode:")
        self.pupil_size_mode = QComboBox()
        self.pupil_size_mode.addItems(("area", "diameter"))

        self.IP_address_tip = QLabel("IP Address:")
        self.IP_address = QLineEdit("127.0.0.1")

        self.send_port_tip = QLabel("Send Port:")
        self.send_port = QSpinBox()
        self.send_port.setEnabled(False)

        self.receive_port_tip = QLabel("Receive Port:")
        self.receive_port = QSpinBox()
        self.receive_port.setEnabled(False)

        # self.ipv46_address_tip = QLabel("Tobii Glasses IPv4/6 Address:")
        self.ipv46_address_tip = QLabel("IPv4/6 Address:")
        self.ipv46_address = QLineEdit("192.168.71.50")
        self.ipv46_address.setEnabled(False)

        # self.UDP_port_tip = QLabel("Tobii Glasses UDP Port:")
        self.UDP_port_tip = QLabel("UDP Port:")
        self.UDP_port = QSpinBox()
        self.UDP_port.setEnabled(False)

        # ******external device***********
        # 是否更新using external device id
        self.update_flag = True

        self.screen_tip = QLabel("Screen:")
        self.screen = QComboBox()
        self.screen.currentTextChanged.connect(self.changeExternalDevice)
        self.sound_tip = QLabel("Sound:")
        self.sound = QComboBox()
        self.screen.currentTextChanged.connect(self.changeExternalDevice)
        for k, v in self.simple_info.items():
            if k.startswith(Info.DEV_SCREEN):
                self.screen.addItem(v)
            elif k.startswith(Info.DEV_SOUND):
                self.sound.addItem(v)

        self.setUI()

        self.using_screen_id = ""
        self.screen_name = ""

        self.using_sound_id = ""
        self.sound_name = ""

    def setUI(self):
        self.device_name_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tracker_type_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tracker_datafile_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.velocity_threshold_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.acceleration_threshold_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.pupil_size_mode_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.IP_address_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.send_port_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.receive_port_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.ipv46_address_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.UDP_port_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.screen_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.sound_tip.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout = QGridLayout()
        layout.addWidget(self.device_name_tip, 0, 0, 1, 1)
        layout.addWidget(self.device_name, 0, 1, 1, 1)
        layout.addWidget(self.tracker_type_tip, 1, 0, 1, 1)
        layout.addWidget(self.tracker_type, 1, 1, 1, 1)
        layout.addWidget(self.calibrate_tracker, 2, 1, 1, 1)
        layout.addWidget(self.calibration_beep, 3, 1, 1, 1)
        layout.addWidget(self.tracker_datafile_tip, 4, 0, 1, 1)
        layout.addWidget(self.tracker_datafile, 4, 1, 1, 1)
        layout.addWidget(self.velocity_threshold_tip, 5, 0, 1, 1)
        layout.addWidget(self.velocity_threshold, 5, 1, 1, 1)
        layout.addWidget(self.acceleration_threshold_tip, 6, 0, 1, 1)
        layout.addWidget(self.acceleration_threshold, 6, 1, 1, 1)
        layout.addWidget(self.force_drift_correction, 7, 1, 1, 1)
        layout.addWidget(self.pupil_size_mode_tip, 8, 0, 1, 1)
        layout.addWidget(self.pupil_size_mode, 8, 1, 1, 1)
        layout.addWidget(self.IP_address_tip, 9, 0, 1, 1)
        layout.addWidget(self.IP_address, 9, 1, 1, 1)
        layout.addWidget(self.send_port_tip, 10, 0, 1, 1)
        layout.addWidget(self.send_port, 10, 1, 1, 1)
        layout.addWidget(self.receive_port_tip, 11, 0, 1, 1)
        layout.addWidget(self.receive_port, 11, 1, 1, 1)
        layout.addWidget(self.ipv46_address_tip, 12, 0, 1, 1)
        layout.addWidget(self.ipv46_address, 12, 1, 1, 1)
        layout.addWidget(self.UDP_port_tip, 13, 0, 1, 1)
        layout.addWidget(self.UDP_port, 13, 1, 1, 1)
        layout.addWidget(self.screen_tip, 14, 0, 1, 1)
        layout.addWidget(self.screen, 14, 1, 1, 1)
        layout.addWidget(self.sound_tip, 15, 0, 1, 1)
        layout.addWidget(self.sound, 15, 1, 1, 1)

        self.setLayout(layout)

    def typeChanged(self, index):
        self.force_drift_correction.setEnabled(index == 2)
        self.pupil_size_mode.setEnabled(index == 2)
        self.IP_address.setEnabled(index == 3)
        self.send_port.setEnabled(index == 3)
        self.receive_port.setEnabled(index == 3)
        self.ipv46_address.setEnabled(index == 8)
        self.UDP_port.setEnabled(index == 8)

    def describe(self, info: dict):
        super(Tracker, self).describe(info)
        self.tracker_type.setCurrentText(info.get("Select Tracker Type", "Simple dummy"))
        self.tracker_datafile.setText(info.get("Eye Tracker Datafile", "automatic"))
        self.calibrate_tracker.setCheckState(info.get("Calibrate Tracker", "") == "Yes")
        self.calibration_beep.setCheckState(info.get("Calibration Beep", "") == "Yes")
        self.velocity_threshold.setValue(int(info.get("Saccade Velocity Threshold", "0")))
        self.acceleration_threshold.setValue(int(info.get("Saccade Acceleration Threshold", "0")))
        self.force_drift_correction.setCheckState((info.get("Force Drift Correction", "") == "Yes") * 2)
        self.pupil_size_mode.setCurrentText(info.get("Pupil Size Mode", "area"))
        self.IP_address.setText(info.get("IP Address", "127.0.0.0"))
        self.send_port.setValue(int(info.get("Send Port", "0")))
        self.receive_port.setValue(int(info.get("Receive Port", "0")))
        self.ipv46_address.setText(info.get("Ipv4/Ipv6 Address", "192.168.71.50"))
        self.UDP_port.setValue(int(info.get("UDP Port", "0")))
        self.screen.setCurrentText(info.get("Screen", "screen_0"))
        self.sound.setCurrentText(info.get("Sound", "sound_0"))
        # screen info
        self.screen_name = self.screen.currentText()
        for k, v in Tracker.simple_info.items():
            if v == self.screen_name:
                self.using_screen_id = k

        self.sound_name = self.sound.currentText()
        for k, v in Tracker.simple_info.items():
            if v == self.sound_name:
                self.using_sound_id = k

    def changeName(self, name: str):
        self.device_name.setText(name)

    def getInfo(self):
        properties: dict = {
            "Device Type": Info.DEV_TRACKER,
            "Device Name": self.device_name.text(),
            "Select Tracker Type": self.tracker_type.currentText(),
            "Calibrate Tracker": self.calibrate_tracker.checkState(),
            "Calibration Beep": self.calibration_beep.checkState(),
            "Eye Tracker Datafile": self.tracker_datafile.text(),
            "Saccade Velocity Threshold": self.velocity_threshold.value(),
            "Saccade Acceleration Threshold": self.acceleration_threshold.value(),
            "Force Drift Correction": self.force_drift_correction.checkState(),
            "Pupil Size Mode": self.pupil_size_mode.currentText(),
            "IP Address": self.IP_address.text(),
            "Send Port": self.send_port.text(),
            "Receive Port": self.receive_port.text(),
            "Ipv4/Ipv6 Address": self.ipv46_address.text(),
            "UDP Port": self.UDP_port.text(),
            "Screen": self.screen.currentText(),
            "Sound": self.sound.currentText(),
        }
        return properties

    def changeExternalDevice(self, device_name: str):
        if self.update_flag:
            if self.sender() == self.screen:
                for k, v in Tracker.simple_info.items():
                    if v == device_name:
                        self.using_screen_id = k

            if self.sender() == self.sound:
                for k, v in Tracker.simple_info.items():
                    if v == device_name:
                        self.using_sound_id = k

    def updateExternalDeviceInformation(self):
        self.update_flag = False
        self.screen.clear()
        self.sound.clear()
        for k, v in self.simple_info.items():
            if k.startswith(Info.DEV_SCREEN):
                self.screen.addItem(v)
            elif k.startswith(Info.DEV_SOUND):
                self.sound.addItem(v)

        if self.using_screen_id in Tracker.simple_info.keys():
            self.screen.setCurrentText(Tracker.simple_info[self.using_screen_id])
        else:
            self.using_screen_id = ""

        if self.using_sound_id in Tracker.simple_info.keys():
            self.sound.setCurrentText(Tracker.simple_info[self.using_sound_id])
        else:
            self.using_sound_id = ""
        self.update_flag = True
