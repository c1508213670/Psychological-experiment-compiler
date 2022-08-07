from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QFormLayout, QCompleter, QGridLayout, QLabel

from app.info import Info
from lib import VarLineEdit, VarComboBox


class RespTrigger(QWidget):
    OUTPUT_DEVICE = []

    def __init__(self, parent=None):
        super(RespTrigger, self).__init__(parent=parent)

        self.using_output_device = {}
        self.current_output_device_id = ""
        self.right = VarLineEdit()
        self.wrong = VarLineEdit()
        self.ignore = VarLineEdit()
        self.resp_trigger_out = QComboBox()
        self.resp_trigger_out.currentTextChanged.connect(self.changeOutput)
        self.resp_trigger_out.addItem("none")
        self.resp_trigger_out.addItems(RespTrigger.OUTPUT_DEVICE)

        self.setUI()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Response Trigger"), 0, 0, 1, 2)
        layout.addWidget(QLabel("Right:"), 1, 0, 1, 1)
        layout.addWidget(self.right, 1, 1, 1, 1)
        layout.addWidget(QLabel("Wrong:"), 1, 2, 1, 1)
        layout.addWidget(self.wrong, 1, 3, 1, 1)
        layout.addWidget(QLabel("None:"), 1, 4, 1, 1)
        layout.addWidget(self.ignore, 1, 5, 1, 1)
        layout.addWidget(QLabel("Device:"), 1, 6, 1, 1)
        layout.addWidget(self.resp_trigger_out, 1, 7, 1, 1)
        self.setLayout(layout)

    def describe(self, info: dict):
        right = info.get("Right")
        wrong = info.get("Wrong")
        ignore = info.get("Ignore")
        output_device_name = info.get("Output Device")
        self.right.setText(right)
        self.wrong.setText(wrong)
        self.ignore.setText(ignore)
        self.resp_trigger_out.setCurrentText(output_device_name)

    def setAttributes(self, attributes):
        self.right.setCompleter(QCompleter(attributes))
        self.wrong.setCompleter(QCompleter(attributes))
        self.ignore.setCompleter(QCompleter(attributes))

    def updateExternalDeviceInformation(self, simple_info: list):
        self.using_output_device.clear()
        self.resp_trigger_out.clear()
        self.resp_trigger_out.addItem("none")
        self.resp_trigger_out.addItems(simple_info)

        output_name = self.using_output_device.get(self.current_output_device_id, "")
        if output_name != "":
            self.resp_trigger_out.setCurrentText(output_name)
        else:
            self.resp_trigger_out.setCurrentIndex(0)

    def changeOutput(self, current_name: str):
        for k, v in self.using_output_device.items():
            if current_name == v:
                self.current_output_device_id = k
                break
        self.right.setEnabled(current_name != "none")
        self.wrong.setEnabled(current_name != "none")
        self.ignore.setEnabled(current_name != "none")

    def getInfo(self):
        info = {
            "Right": self.right.text(),
            "Wrong": self.wrong.text(),
            "No Resp": self.ignore.text(),
            "Output Device": self.resp_trigger_out.currentText(),
        }
        return info


class EyeAction(QWidget):
    def __init__(self, parent=None):
        super(EyeAction, self).__init__(parent)

        self.start = VarLineEdit()
        self.end = VarLineEdit()
        self.mean = VarLineEdit()
        self.is_oval = QComboBox()
        self.is_oval.addItems(("No", "Yes"))

        self.setUI()

    def setUI(self):
        layout = QGridLayout()
        layout.addWidget(QLabel("Correct Gaze within ROI (e.g., x0,y0,x1,y1)"), 0, 0, 1, 8)
        layout.addWidget(QLabel("Start:"), 1, 0, 1, 1)
        layout.addWidget(self.start, 1, 1, 1, 1)
        layout.addWidget(QLabel("  End:"), 1, 2, 1, 1)
        layout.addWidget(self.end, 1, 3, 1, 1)
        layout.addWidget(QLabel("  Mean:"), 1, 4, 1, 1)
        layout.addWidget(self.mean, 1, 5, 1, 1)
        layout.addWidget(QLabel("IsOval:"), 1, 6, 1, 1)
        layout.addWidget(self.is_oval, 1, 7, 1, 1)
        self.setLayout(layout)

    def describe(self, info: dict):
        device_id: str = info.get("Device Id")

        start = info.get("Start")
        end = info.get("End")
        mean = info.get("Mean")
        is_oval = info.get("Is Oval")
        self.start.setText(start)
        self.start.setToolTip("An rect define by a 1x4 vector(e.g., x0,y0,x1,y1)")
        self.end.setText(end)
        self.end.setToolTip("An rect define by a 1x4 vector(e.g., x0,y0,x1,y1)")
        self.mean.setText(mean)
        self.mean.setToolTip("An rect define by a 1x4 vector(e.g., x0,y0,x1,y1)")
        self.is_oval.setCurrentText(is_oval)
        self.setEnabled(device_id.startswith(Info.DEV_EYE_ACTION))

    def setAttributes(self, attributes):
        self.start.setCompleter(QCompleter(attributes))
        self.end.setCompleter(QCompleter(attributes))
        self.mean.setCompleter(QCompleter(attributes))

    def getInfo(self):
        info = {
            "Start": self.start.text(),
            "End": self.end.text(),
            "Mean": self.mean.text(),
            "Is Oval": self.is_oval.currentText(),
        }
        return info


class RespInfo(QWidget):
    def __init__(self, device_type: str, parent=None):
        super(RespInfo, self).__init__(parent=parent)

        self.device_label = QLabel()
        self.allowable = VarLineEdit()
        self.device_type = device_type

        if device_type == Info.DEV_MOUSE:
            self.allowable.setToolTip("1,2,3 for left, right, and middle key respectively")
        elif device_type == Info.DEV_EYE_ACTION:
            self.allowable.setToolTip("3, 4, 5, 6, 7, 8, 9 for start blink, end blink, start saccade, end saccade, start fixation, end fixation, and fixation update, respectively")
        elif device_type == Info.DEV_KEYBOARD:
            self.allowable.setToolTip("Use {keyNames} to define key names longer than 1 char, e.g., {space} for the space key.\n "
                                      "See all key names list by running the command KbName([1:255]) in MATLAB.")
        elif device_type == Info.DEV_GAMEPAD:
            self.allowable.setToolTip("1 to 8 for the keys in Gamepad (Note, not all gamepad have 8 keys)")

        self.correct = VarLineEdit()
        if device_type == Info.DEV_MOUSE:
            self.correct.setToolTip("1,2,3 for left, right, and middle key respectively")
        elif device_type == Info.DEV_EYE_ACTION:
            self.correct.setToolTip("3, 4, 5, 6, 7, 8, 9 for start blink, end blink, start saccade, end saccade, start fixation, end fixation, and fixation update, respectively")
        elif device_type == Info.DEV_KEYBOARD:
            self.correct.setToolTip("Use {keyNames} to define key names longer than 1 char, e.g., {space} for the space key.\n "
                                      "See all key names list by running the command KbName([1:255]) in MATLAB.")
        self.RT_window = VarComboBox(True)
        self.RT_window.setAcceptDrops(False)
        self.RT_window.addItems(["(Same as duration)", "(End of timeline)", "1000", "2000", "3000", "4000", "5000"])

        self.end_action = VarComboBox()
        self.end_action.setAcceptDrops(False)

        if device_type == Info.DEV_EYE_ACTION:
            self.end_action.addItems(["Terminate", "(None)"])
        else:
            self.end_action.addItems(["Terminate", "Terminate Till Release", "(None)"])
        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.addRow("Response:", self.device_label)
        layout.addRow("Allowable:", self.allowable)
        layout.addRow("Correct:", self.correct)
        layout.addRow("RT Window:", self.RT_window)
        layout.addRow("Response Action:", self.end_action)
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.setVerticalSpacing(20)
        layout.setContentsMargins(10, 0, 0, 0)
        self.setLayout(layout)

    def describe(self, info: dict):
        device_name = info.get("Device Name")
        allowable = info.get("Allowable")
        correct = info.get("Correct")
        rt_window = info.get("RT Window")
        end_action = info.get("End Action")

        self.device_label.setText(device_name)
        self.allowable.setText(allowable)
        self.correct.setText(correct)
        self.RT_window.setCurrentText(rt_window)
        self.end_action.setCurrentText(end_action)

    def changeName(self, new_name: str):
        self.device_label.setText(new_name)

    def setAttributes(self, attributes):
        self.allowable.setCompleter(QCompleter(attributes))
        self.correct.setCompleter(QCompleter(attributes))

    def getInfo(self):
        info = {
            "Device Name": self.device_label.text(),
            "Device Type": self.device_type,
            "Allowable": self.allowable.text(),
            "Correct": self.correct.text(),
            "RT Window": self.RT_window.currentText(),
            "End Action": self.end_action.currentText(),
        }
        return info
