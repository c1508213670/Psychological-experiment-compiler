from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QPushButton

from app.func import Func
from app.info import Info
from lib import VarComboBox


class PtbPref(QWidget):
    def __init__(self, parent=None):
        super(PtbPref, self).__init__(parent=parent)

        self.default_properties = Info.PTB_PREF

        self.default_properties.update({
            "Visual Debug Level": "-1: Do nothing",
            "Suppress All Warnings": "No",
            "Verbosity Level": "4: More useful info (default)",
            "Syncing Test Level": "0: Enable syncing test (default)",
            "Trigger Synchronize Displays": "No",
            "Suppress Keypress Output": "No",
            "M File Encoding Format": "GBK"
        })

        self.setWindowTitle("Psychtoolbox Preference")
        self.setWindowModality(2)
        self.setWindowIcon(QIcon(Func.getImage("common/icon.png")))
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, Qt.white)
        self.setPalette(p)

        self.verbosity_box = VarComboBox()
        self.verbosity_box.setAcceptDrops(False)
        self.verbosity_box.setEditable(False)
        self.verbosity_box.addItems(
            ("4: More useful info (default)", "0: Shut up", "1: Print errors", "2: Also warnings", "3: Also some info", "5: Be very verbose"))
        self.verbosity_box.setItemData(0, "4: Print more useful info", Qt.ToolTipRole)
        self.verbosity_box.setItemData(1, "0: Print None information", Qt.ToolTipRole)
        self.verbosity_box.setItemData(2, "1: Print errors", Qt.ToolTipRole)
        self.verbosity_box.setItemData(3, "2: Print also warnings", Qt.ToolTipRole)
        self.verbosity_box.setItemData(4, "3: Print also some useful info", Qt.ToolTipRole)
        self.verbosity_box.setItemData(5, ">5 Be very verbose (mostly for debugging the driver itself)", Qt.ToolTipRole)
        self.verbosity_box.setToolTip("Set level of verbosity for error/warning/status messages")

        self.visual_debug_level_box = VarComboBox()
        self.visual_debug_level_box.setAcceptDrops(False)
        self.visual_debug_level_box.setEditable(False)
        self.visual_debug_level_box.addItems(
            ("-1: Do nothing", "0: Shut up", "1: Only errors (black startup screen)", "2: Also warnings", "3: Disable startup msg", "4: Also blue bootup screen", "5: Also visual test sheets"))
        self.visual_debug_level_box.setItemData(0, "-1: Do nothing", Qt.ToolTipRole)
        self.visual_debug_level_box.setItemData(1, "0: Shut up (disable all visual alerts, e.g., the red flashing warning sign)", Qt.ToolTipRole)
        self.visual_debug_level_box.setItemData(2, "1: Print errors (will also enable the black startup screen)", Qt.ToolTipRole)
        self.visual_debug_level_box.setItemData(3, "2: Print also warnings", Qt.ToolTipRole)
        self.visual_debug_level_box.setItemData(4, "3: Disable startup msg (prevents the ptb startup message ''Welcome to the Psychtoolbox...'')", Qt.ToolTipRole)
        self.visual_debug_level_box.setItemData(5, "4: Also blue bootup screen", Qt.ToolTipRole)
        self.visual_debug_level_box.setItemData(5, "5: Also visual test sheets", Qt.ToolTipRole)
        self.visual_debug_level_box.setToolTip("extract information from ScreenPreferenceState.c")

        self.suppress_all_warnings_box = VarComboBox()
        self.suppress_all_warnings_box.setAcceptDrops(False)
        self.suppress_all_warnings_box.setEditable(False)
        self.suppress_all_warnings_box.addItems(
            ("No", "Yes"))
        self.suppress_all_warnings_box.setToolTip("Disable all warning messages output to the command window or not")

        self.syncing_test_level_box = VarComboBox()
        self.syncing_test_level_box.setAcceptDrops(False)
        self.syncing_test_level_box.setEditable(False)
        self.syncing_test_level_box.addItems(
            ("0: Enable syncing test (default)", "1: Shorten syncing test", "2: Disable syncing test"))
        self.syncing_test_level_box.setItemData(0, "0: Enable the syncing test and abort your script if the syncing tests failed", Qt.ToolTipRole)
        self.syncing_test_level_box.setItemData(1, "1: Shorten syncing test and will force PTB to continue if the syncing tests failed", Qt.ToolTipRole)
        self.syncing_test_level_box.setItemData(2, "2: Totally disable the syncing tests", Qt.ToolTipRole)

        self.synchronize_displays_box = VarComboBox()
        self.synchronize_displays_box.setAcceptDrops(False)
        self.synchronize_displays_box.setEditable(False)
        self.synchronize_displays_box.addItems(
            ("No", "Yes"))
        self.synchronize_displays_box.setItemData(0, "Do nothing", Qt.ToolTipRole)
        self.synchronize_displays_box.setItemData(1, "Trigger a instantaneous synchronization of all available display heads, if possible", Qt.ToolTipRole)

        self.suppress_kb_out_box = VarComboBox()
        self.suppress_kb_out_box.setAcceptDrops(False)
        self.suppress_kb_out_box.setEditable(False)
        self.suppress_kb_out_box.addItems(
            ("No", "Yes"))
        self.suppress_kb_out_box.setItemData(0, "Do nothing", Qt.ToolTipRole)
        self.suppress_kb_out_box.setItemData(1, "Use listenChar(-1) to suppress keypress output into the Matlab/Octave command window", Qt.ToolTipRole)

        self.encoding_type_box = VarComboBox()
        self.encoding_type_box.setAcceptDrops(False)
        self.encoding_type_box.setEditable(False)
        self.encoding_type_box.addItems(
            ("GBK", "utf-8"))
        self.encoding_type_box.setItemData(0, "GBK: character set for Simplified Chinese characters", Qt.ToolTipRole)
        self.encoding_type_box.setItemData(1, "UTF-8: 8-bit Unicode Transformation Format", Qt.ToolTipRole)
        self.encoding_type_box.setToolTip("Set encoding type for the output m file")



        # bottom
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")

        self.ok_bt.clicked.connect(self.ok)
        self.cancel_bt.clicked.connect(self.cancel)
        self.apply_bt.clicked.connect(self.apply)

        self.setUI()

    def setUI(self):

        l00 = QLabel("Suppress All Warnings Level:")
        l10 = QLabel("Visual Debug Level:")
        l20 = QLabel("Verbosity Level:")
        l30 = QLabel("Syncing Test Level:")
        l40 = QLabel("Trigger Synchronize Displays:")
        l50 = QLabel("Suppress Keypress Output:")
        l60 = QLabel("M file Encoding Format:")

        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l40.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l50.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l60.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("")
        layout1 = QGridLayout()

        layout1.addWidget(l00, 0, 0)
        layout1.addWidget(self.suppress_all_warnings_box, 0, 1)

        layout1.addWidget(l40, 1, 0)
        layout1.addWidget(self.synchronize_displays_box, 1, 1)

        layout1.addWidget(l50, 2, 0)
        layout1.addWidget(self.suppress_kb_out_box, 2, 1)

        layout1.addWidget(l10, 3, 0)
        layout1.addWidget(self.visual_debug_level_box, 3, 1)

        layout1.addWidget(l20, 4, 0)
        layout1.addWidget(self.verbosity_box, 4, 1)

        layout1.addWidget(l30, 5, 0)
        layout1.addWidget(self.syncing_test_level_box, 5, 1)

        layout1.addWidget(l60, 6, 0)
        layout1.addWidget(self.encoding_type_box, 6, 1)

        group1.setLayout(layout1)

        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(group1, 5)
        layout.addSpacing(1)
        layout.addLayout(below_layout, 1)
        layout.setSpacing(10)

        self.setLayout(layout)

    def ok(self):
        self.apply()
        self.close()

    def cancel(self):
        self.loadSetting()

    def apply(self):
        self.updateInfo()

    def updateInfo(self):
        self.default_properties["Visual Debug Level"] = self.visual_debug_level_box.currentText()
        self.default_properties["Suppress All Warnings"] = self.suppress_all_warnings_box.currentText()
        self.default_properties["Verbosity Level"] = self.verbosity_box.currentText()
        self.default_properties["Syncing Test Level"] = self.syncing_test_level_box.currentText()
        self.default_properties["Trigger Synchronize Displays"] = self.synchronize_displays_box.currentText()
        self.default_properties["Suppress Keypress Output"] = self.suppress_kb_out_box.currentText()
        self.default_properties["M File Encoding Format"] = self.encoding_type_box.currentText()

    def loadSetting(self):
        self.visual_debug_level_box.setCurrentText(self.default_properties["Visual Debug Level"])
        self.suppress_all_warnings_box.setCurrentText(self.default_properties["Suppress All Warnings"])
        self.verbosity_box.setCurrentText(self.default_properties["Verbosity Level"])
        self.syncing_test_level_box.setCurrentText(self.default_properties["Syncing Test Level"])
        self.synchronize_displays_box.setCurrentText(self.default_properties["Trigger Synchronize Displays"])
        self.suppress_kb_out_box.setCurrentText(self.default_properties["Suppress Keypress Output"])
        self.encoding_type_box.setCurrentText(self.default_properties["M File Encoding Format"])
