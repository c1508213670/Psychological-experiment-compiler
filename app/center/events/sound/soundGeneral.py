from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QPushButton, QCheckBox, \
    QFileDialog, QCompleter, QSizePolicy, QComboBox

from app.func import Func
from lib import VarLineEdit, VarComboBox


# sound event专属页面
class SoundTab1(QWidget):
    def __init__(self, parent=None):
        super(SoundTab1, self).__init__(parent)
        self.default_properties = {
            "File Name": "",
            "Buffer Size": "5000",
            "Stream Refill": "0",
            "Start Offset": "0",
            "Stop Offset": "0",
            "Repetitions": "1",
            "Volume Control": 0,
            "Volume": "1",
            "Latency Bias": 0,
            "Bias Time": "0",
            "Sound Device": "",
            "Wait For Start": "No",
            "Sync To Vbl": 1,
            "Clear After": "clear_0",
            "Screen Name": "screen_0"
        }
        self.file_name = VarLineEdit()
        self.open_bt = QPushButton("Open file")
        self.open_bt.clicked.connect(self.openFile)

        self.volume_control = QCheckBox("Volume Control (0~1):")  # Volume control
        self.volume_control.setLayoutDirection(Qt.RightToLeft)

        self.volume_control.stateChanged.connect(self.volumeChecked)

        self.volume = VarLineEdit()
        self.volume.setText("1")

        self.latency_bias = QCheckBox("Latency Bias (ms):")  # Latency Bias
        self.latency_bias.setLayoutDirection(Qt.RightToLeft)

        self.latency_bias.stateChanged.connect(self.latencyBiasChecked)

        self.bias_time = VarLineEdit()
        self.bias_time.setText("0")

        self.buffer_size = VarLineEdit("500")
        self.stream_refill = VarComboBox()

        self.start_offset = VarLineEdit("0")
        self.stop_offset = VarLineEdit("0")
        self.repetitions = VarLineEdit("1")

        self.using_sound_id: str = ""
        self.sound = QComboBox()
        self.sound_info = Func.getDeviceInfo("sound")
        self.sound.addItems(self.sound_info.values())
        self.sound.currentTextChanged.connect(self.changeSound)

        self.wait_for_start = VarComboBox()
        self.wait_for_start.addItems(("No", "Yes"))

        # added by yang
        self.sync_to_vbl = QCheckBox("Sync to Screen VBL:")  # Latency Bias
        self.sync_to_vbl.setLayoutDirection(Qt.RightToLeft)
        self.sync_to_vbl.setChecked(True)

        self.sync_to_vbl.stateChanged.connect(self.syncToVblChecked)

        self.clear_after = VarComboBox()
        self.clear_after.addItems(("clear_0", "notClear_1", "doNothing_2"))
        self.clear_after.setEnabled(self.sync_to_vbl.checkState())

        self.using_screen_id: str = ""
        self.screen_name = QComboBox()
        self.screen_info = Func.getDeviceInfo("screen")
        self.screen_name.addItems(self.screen_info.values())
        self.screen_name.currentTextChanged.connect(self.changeScreen)
        self.screen_name.setEnabled(self.sync_to_vbl.checkState())

        self.setGeneral()

    def setGeneral(self):
        self.start_offset.setRegularExpress(VarLineEdit.Integer)
        self.stop_offset.setRegularExpress(VarLineEdit.Integer)
        self.repetitions.setRegularExpress(r"(\d+)|(\d*\.?\d{,2})")

        self.stream_refill.addItems(["0", "1", "2"])
        self.volume.setEnabled(False)
        self.bias_time.setEnabled(False)

        l0 = QLabel("File Name:")
        l1 = QLabel("Buffer Size (ms):")
        l2 = QLabel("Stream Refill:")
        l3 = QLabel("Start Offset (ms):")
        l4 = QLabel("Stop Offset (ms):")
        l5 = QLabel("Repetition(s):")
        l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("File")
        layout1 = QGridLayout()
        layout1.addWidget(l0, 0, 0, 1, 1)
        layout1.addWidget(self.file_name, 0, 1, 1, 2)
        layout1.addWidget(self.open_bt, 0, 3, 1, 1)

        layout1.addWidget(l2, 2, 0)
        layout1.addWidget(self.stream_refill, 2, 1)

        layout1.addWidget(l3, 3, 0)
        layout1.addWidget(self.start_offset, 3, 1)
        layout1.addWidget(l4, 4, 0)
        layout1.addWidget(self.stop_offset, 4, 1)

        layout1.addWidget(l5, 5, 0)
        layout1.addWidget(self.repetitions, 5, 1)

        group1.setLayout(layout1)

        l6 = QLabel("Sound Device:")
        l7 = QLabel("Wait For Start:")
        l8 = QLabel("Don't Clear After:")

        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group2 = QGroupBox("Control && Device")
        layout2 = QGridLayout()

        self.bias_time.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.volume.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        layout2.addWidget(self.sync_to_vbl, 0, 0, )
        layout2.addWidget(self.screen_name, 0, 1, )
        layout2.addWidget(l8, 0, 2)
        layout2.addWidget(self.clear_after, 0, 3)

        layout2.addWidget(self.volume_control, 1, 0, )
        layout2.addWidget(self.volume, 1, 1, )
        layout2.addWidget(l6, 1, 2)
        layout2.addWidget(self.sound, 1, 3)

        layout2.addWidget(self.latency_bias, 2, 0)
        layout2.addWidget(self.bias_time, 2, 1)
        # layout2.addWidget(l7, 2, 2)
        # layout2.addWidget(self.wait_for_start, 2, 3)

        group2.setLayout(layout2)

        layout = QVBoxLayout()

        layout.addWidget(group1, 2)
        layout.addWidget(group2, 1)

        self.setLayout(layout)

    def refresh(self):
        # refresh sound Dev
        self.sound_info = Func.getDeviceInfo("sound")
        sound_id = self.using_sound_id
        self.sound.clear()
        self.sound.addItems(self.sound_info.values())
        sound_name = self.sound_info.get(sound_id)
        if sound_name:
            self.sound.setCurrentText(sound_name)
            self.using_sound_id = sound_id

        # refresh screen
        self.screen_info = Func.getDeviceInfo("screen")
        screen_id = self.using_screen_id
        self.screen_name.clear()
        self.screen_name.addItems(self.screen_info.values())
        screen_name = self.screen_info.get(screen_id)
        if screen_name:
            self.screen_name.setCurrentText(screen_name)
            self.using_screen_id = screen_id

        self.updateInfo()

    def changeSound(self, sound):
        for k, v in self.sound_info.items():
            if v == sound:
                self.using_sound_id = k
                break

    def changeScreen(self, screen):
        for k, v in self.screen_info.items():
            if v == screen:
                self.using_screen_id = k
                break

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the sound file", Func.getFullFilePath(self.file_name.text()),
                                                   "Sound File (*)", options=options)
        file_name = Func.getRelativeFilePath(file_name)
        if file_name:
            self.file_name.setText(file_name)

    def volumeChecked(self, e):
        if e == 2:
            self.volume.setEnabled(True)
        else:
            self.volume.setEnabled(False)

    def latencyBiasChecked(self, e):
        if e == 2:
            self.bias_time.setEnabled(True)
        else:
            self.bias_time.setEnabled(False)

    def syncToVblChecked(self, e):
        if e == 2:
            self.clear_after.setEnabled(True)
            self.screen_name.setEnabled(True)
        else:
            self.clear_after.setEnabled(False)
            self.screen_name.setEnabled(False)

    def setAttributes(self, attributes: list):
        self.file_name.setCompleter(QCompleter(attributes))
        self.buffer_size.setCompleter(QCompleter(attributes))
        self.start_offset.setCompleter(QCompleter(attributes))
        self.stop_offset.setCompleter(QCompleter(attributes))
        self.repetitions.setCompleter(QCompleter(attributes))
        self.volume.setCompleter(QCompleter(attributes))
        self.bias_time.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        self.default_properties["File Name"] = self.file_name.text()
        self.default_properties["Buffer Size"] = self.buffer_size.text()
        self.default_properties["Stream Refill"] = self.stream_refill.currentText()
        self.default_properties["Start Offset"] = self.start_offset.text()
        self.default_properties["Stop Offset"] = self.stop_offset.text()
        self.default_properties["Repetitions"] = self.repetitions.text()
        self.default_properties["Volume Control"] = self.volume_control.checkState()
        self.default_properties["Volume"] = self.volume.text()
        self.default_properties["Latency Bias"] = self.latency_bias.checkState()
        self.default_properties["Bias Time"] = self.bias_time.text()
        self.default_properties["Sound Device"] = self.sound.currentText()
        self.default_properties["Wait For Start"] = self.wait_for_start.currentText()
        self.default_properties["Sync To Vbl"] = self.sync_to_vbl.checkState()
        self.default_properties["Clear After"] = self.clear_after.currentText()
        self.default_properties["Screen name"] = self.screen_name.currentText()

    def getProperties(self):
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File Name"])
        self.buffer_size.setText(self.default_properties["Buffer Size"])
        self.stream_refill.setCurrentText(self.default_properties["Stream Refill"])
        self.start_offset.setText(self.default_properties["Start Offset"])
        self.stop_offset.setText(self.default_properties["Stop Offset"])
        self.repetitions.setText(self.default_properties["Repetitions"])
        self.volume_control.setCheckState(self.default_properties["Volume Control"])
        self.volume.setText(self.default_properties["Volume"])
        self.latency_bias.setCheckState(self.default_properties["Latency Bias"])
        self.bias_time.setText(self.default_properties["Bias Time"])
        self.sound.setCurrentText((self.default_properties["Sound Device"]))
        self.wait_for_start.setCurrentText(self.default_properties["Wait For Start"])
        self.sync_to_vbl.setCheckState(self.default_properties["Sync To Vbl"])
        self.clear_after.setCurrentText(self.default_properties["Clear After"])
        self.screen_name.setCurrentText(self.default_properties["Screen Name"])
