import os
import re

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import QTextEdit, QApplication, QFileDialog, QLabel, QMenu, QGridLayout, \
    QFrame, QActionGroup

from app.func import Func
from app.info import Info
from lib import HoverButton, Settings


class Version(QTextEdit):
    def __init__(self, name: str, version: str):
        super(Version, self).__init__()
        self.setReadOnly(True)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setStyleSheet("""
            border: none;
            background: transparent;
        """)
        # set text
        self.setAlignment(Qt.AlignHCenter)
        if Info.OS_TYPE == 1:
            cFontTypeStr = "Gen Shin Gothic"
        else:
            cFontTypeStr = "Gen Shin Gothic Light"

        if Info.IS_RETINA_SCR_LINUX:
            name_font_size = 32*2
            ver_font_size = 18*2
        else:
            name_font_size = 32
            ver_font_size = 18

        self.setText(f"""
        <div style="text-align: center;">
            <span style="color:rgb(64,64,64);font-size:{name_font_size}px; font-family: '{cFontTypeStr}'">
                {name}
            </span>
            <br/>
            <span style="color:rgb(157,157,157); font-size:{ver_font_size}px; font-family: '{cFontTypeStr}'">
                {version}
            </span>
        </div>
        """)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def enterEvent(self, QEvent):
        super(Version, self).enterEvent(QEvent)
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    def leaveEvent(self, QEvent):
        super(Version, self).leaveEvent(QEvent)
        QApplication.restoreOverrideCursor()


class FileButtonArea(QFrame):
    fileCreated = pyqtSignal(str)
    fileOpened = pyqtSignal(str)

    def __init__(self):
        super(FileButtonArea, self).__init__()
        self.setObjectName("FileButtonArea")
        self.setStyleSheet(f"""
        QFrame#FileButtonArea {{
            border-image: url({Func.getImageForStyleSheet("common/background.png")});
        }}
        """)

        if Info.IS_RETINA_SCR_LINUX:
            self.setFixedWidth(1000)
            iconSize = QSize(120, 120)
        else:
            self.setFixedWidth(500)
            iconSize = QSize(60, 60)

        # widget
        icon = QLabel()
        icon.setPixmap(Func.getImageObject("common/icon.png", type=0, size=iconSize))
        icon.setStyleSheet("background:transparent;")
        # menu
        self.menu = QMenu()
        #
        self.default_mode_action = self.menu.addAction("Default Mode", lambda: self.changeOpenMode("default mode"))
        self.open_blank_file_action = self.menu.addAction("Open Blank File", lambda: self.changeOpenMode("open blank file"))

        if Info.OS_TYPE == 0:
            self.default_mode_action.setIcon(Func.getImageObject("menu/checked", 1, size=iconSize))
            self.open_blank_file_action.setIcon(Func.getImageObject("menu/checked", 1, size=iconSize))
        else:
            self.default_mode_action.setCheckable(True)
            self.open_blank_file_action.setCheckable(True)

            self.open_mode_group = QActionGroup(self)
            self.open_mode_group.setExclusive(True)

            self.open_mode_group.addAction(self.default_mode_action)
            self.open_mode_group.addAction(self.open_blank_file_action)

        open_mode = Settings("config.ini", Settings.IniFormat).value("open_mode", "default mode")
        self.changeOpenMode(open_mode)

        # buttons
        create_button = HoverButton("menu/add", "Create New File")
        create_button.clicked.connect(self.handleCreateButtonClicked)
        open_button = HoverButton("menu/open", "Open")
        open_button.clicked.connect(self.handleOpenButtonClicked)
        setting_button = HoverButton("menu/setting", "Change Open Mode")
        setting_button.clicked.connect(
            lambda checked: self.menu.exec(self.mapToGlobal(setting_button.pos())))
        # layout
        layout = QGridLayout()
        # total number of columns
        total_columns = 18
        button_start_column = 8

        for i in range(total_columns):
            layout.setColumnStretch(i, 1)
        layout.setRowStretch(0, 2)
        layout.addWidget(icon, 1, 1, 1, total_columns - 2, Qt.AlignHCenter)
        layout.setRowStretch(1, 12)
        layout.addWidget(Version("PsyBuilder", "Version 0.1"), 2, 1, 1, total_columns - 2)
        layout.setRowStretch(2, 12)
        layout.addWidget(create_button, 3, button_start_column, 1, 1, Qt.AlignLeft)
        layout.setRowStretch(3, 1)
        layout.addWidget(open_button, 4, button_start_column, 1, 1, Qt.AlignLeft)
        layout.setRowStretch(4, 1)
        layout.addWidget(setting_button, 5, button_start_column, 1, 1, Qt.AlignLeft)
        layout.setRowStretch(5, 1)
        layout.setRowStretch(6, 20)
        self.setLayout(layout)

    def handleCreateButtonClicked(self, checked):
        """

        :return:
        """
        directory = Settings("config.ini", Settings.IniFormat).value("file_directory", "")
        if not directory:
            # in order to compatible with pyinstaller
            # directory = os.getcwd()
            # directory = os.path.dirname(os.path.abspath(__file__))
            directory = Info.BasePath
        file_path, _ = QFileDialog().getSaveFileName(self, "Create file", directory, "Psy Files (*.psy);")
        # file_path, _ = QFileDialog().getSaveFileName(self, "Create file", directory, "Psy Files (*.psy);",options = QFileDialog.DontUseNativeDialog)
        if file_path:
            if not re.search(r"\.psy$", file_path):
                file_path = file_path + ".psy"
            self.fileCreated.emit(file_path)

    def handleOpenButtonClicked(self, checked):
        """

        :return:
        """
        directory = Settings("config.ini", Settings.IniFormat).value("file_directory", "")
        if not directory:
            # directory = os.getcwd()
            directory = os.path.dirname(os.path.abspath(__file__))
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose File", directory, "Psy File (*.psy)")
        if file_path:
            self.fileOpened.emit(file_path)

    def changeOpenMode(self, mode: str):
        """
        change open mode in config and menu
        """
        # config
        Settings("config.ini", Settings.IniFormat).setValue("open_mode", mode)
        # menu

        if Info.OS_TYPE == 0:
            isSetIcoVisible = ("default mode" == mode)
            self.default_mode_action.setIconVisibleInMenu(isSetIcoVisible)
            self.open_blank_file_action.setIconVisibleInMenu(not isSetIcoVisible)
        else:
            if "default mode" == mode:
                self.default_mode_action.setChecked(True)
            else:
                self.open_blank_file_action.setChecked(True)