from PyQt5.QtCore import QUrl, Qt, QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QAction, QToolBar, QPushButton, QSlider, QWidget, \
    QGridLayout, QLabel, QVBoxLayout

from app.func import Func
from lib import MessageBox, TabItemMainWindow
from .soundProperty import SoundProperty


class SoundDisplay(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(SoundDisplay, self).__init__(widget_id, widget_name)
        self.file: str = ""
        self.is_loop: bool = False

        self.volume: int = 100
        self.pro_window = SoundProperty()

        self.default_properties = self.pro_window.default_properties

        self.play_bt = QPushButton("")
        self.play_bt.setIcon(QIcon(Func.getImage("operate/start_video.png")))
        self.player = QMediaPlayer()

        self.player_list = QMediaPlaylist()

        self.play_bt.setEnabled(False)
        self.progress_bar = QSlider()
        self.progress_bar.setOrientation(Qt.Horizontal)

        self.tip = QLabel()
        self.tip1 = QLabel()
        self.tip2 = QLabel()

        self.center = QWidget()

        self.setUI()
        self.linkSignal()

    def setUI(self):
        self.setWindowTitle("SoundDisplay")
        self.play_bt.setFixedSize(120, 120)
        self.play_bt.setMaximumHeight(120)
        self.play_bt.setMinimumHeight(120)
        self.play_bt.setMaximumWidth(120)
        self.play_bt.setMinimumWidth(120)
        self.tip.setMaximumHeight(20)
        self.tip.setAlignment(Qt.AlignCenter)
        self.tip.setText("Load your audio first!")
        self.tip1.setText("00:00.000")
        self.tip1.setAlignment(Qt.AlignRight)
        self.tip2.setText("00:00.000")

        # center = QWidget()

        layout = QVBoxLayout()
        layout.addWidget(QLabel(""), 2)
        layout.addWidget(self.play_bt, 2, Qt.AlignHCenter)
        layout.addWidget(self.tip, 1, Qt.AlignCenter)
        layout2 = QGridLayout()
        layout2.addWidget(self.progress_bar, 0, 1, 1, 4)
        layout2.addWidget(self.tip1, 0, 0, 1, 1)
        layout2.addWidget(self.tip2, 0, 5, 1, 1)
        layout2.setHorizontalSpacing(10)

        layout.addLayout(layout2)
        layout.addWidget(QLabel(), 2)
        layout.setSpacing(0)
        layout.setContentsMargins(10, 40, 10, 40)

        self.center.setLayout(layout)
        self.setCentralWidget(self.center)

        # self.center.setStyleSheet("background-color: rgb({});".format("0,255,0"))
        # center.setLayout(layout)
        # self.setCentralWidget(center)

        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImage("menu/setting.png")), "setting", self)
        open_pro.triggered.connect(self.openSettingWindow)

        tool.addAction(open_pro)

        self.addToolBar(Qt.TopToolBarArea, tool)

    def linkSignal(self):
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.player.stateChanged.connect(self.changeIcon)
        self.player.durationChanged.connect(self.changeTip)
        self.player.positionChanged.connect(self.positionChanged)
        self.play_bt.clicked.connect(self.playSound)
        self.progress_bar.sliderMoved.connect(self.setPosition)

    def refresh(self):
        self.pro_window.refresh()
        self.setScrBackgroundColor()

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.updateInfo()
        self.parseProperties()
        file_name = self.pro_window.general.file_name.text()
        file_name = Func.getFullFilePath(file_name)
        if Func.isRef(file_name):
            file_name = ""
            self.file = ""
        if file_name:
            if QFileInfo(file_name).isFile():
                # 音频文件名
                try:
                    audio_name = ".".join(file_name.split("/")[-1].split(".")[0:-1])
                except Exception:
                    audio_name = "audio"
                # 避免重复加载文件
                if file_name != self.file:
                    self.file = file_name
                    self.player_list.clear()
                    self.player_list.addMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
                    self.player.setPlaylist(self.player_list)
                    self.tip1.setText("00:00.000")
                    self.tip2.setText("00:00.000")
                    self.progress_bar.setRange(0, 0)
                # 循环播放否
                if self.is_loop:
                    self.player_list.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
                else:
                    self.player_list.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)
                self.play_bt.setEnabled(True)
                self.tip.setText(audio_name)
            else:
                # self.pro_window.setWindowFlag(Qt.CustomizeWindowHint)
                self.pro_window.close()
                MessageBox.warning(self, "Warning", "The file path is invalid!", MessageBox.Ok)

        else:
            self.play_bt.setEnabled(False)
            self.tip.setText("Load your audio first!")

        self.propertiesChanged.emit(self.widget_id)

        self.setScrBackgroundColor()

    def parseProperties(self):
        if self.pro_window.general.repetitions.text() != "0":
            self.is_loop = True
        else:
            self.is_loop = False
        volume_control = self.pro_window.general.volume_control.checkState()
        if volume_control:
            volume_ = self.pro_window.general.volume.text()
            if volume_.isdigit():
                self.volume = int(volume_)


    def setScrBackgroundColor(self):
        color = Func.getCurrentScreenColor(self.pro_window.getScreenId())
        self.center.setStyleSheet("background-color: rgb({});".format(color))

    def setLabel(self):
        m = int(self.player.duration() / (1000 * 60))
        s = int(self.player.duration() / 1000 - m * 60)
        x = int(self.player.duration() % 1000)
        self.tip2.setText('{:0>2d}:{:0>2d}.{:0>3d}'.format(m, s, x))

    def changeTip(self, duration):
        m = int(duration / (1000 * 60))
        s = int(duration / 1000 - m * 60)
        x = int(duration % 1000)
        self.progress_bar.setRange(0, duration)
        self.tip2.setText('{:0>2d}:{:0>2d}.{:0>3d}'.format(m, s, x))

    def playSound(self):
        if not self.player.isAudioAvailable():
            self.player_list.clear()
            MessageBox.warning(self, "Invalid Audio File", "Please open the audio file", MessageBox.Ok)
        else:
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.pause()
            elif self.player.state() == QMediaPlayer.PausedState:
                self.player.play()
            else:
                self.player.play()
                self.player.setVolume(self.volume)

    # 拖动进度
    def setPosition(self, position):
        self.player.setPosition(position)
        m = int(position / (1000 * 60))
        s = int(position / 1000 - m * 60)
        self.tip1.setText('{:0>2d}:{:0>2d}'.format(m, s))

    # 按进度移动
    def positionChanged(self, position):
        self.progress_bar.setValue(position)
        m = int(position / (1000 * 60))
        s = int(position / 1000 - m * 60)
        x = position % 1000
        self.tip1.setText('{:0>2d}:{:0>2d}.{:0>3d}'.format(m, s, x))

    def changeIcon(self, statue):
        if statue == QMediaPlayer.PlayingState:
            self.play_bt.setIcon(QIcon(Func.getImage("operate/pause_video.png")))
        else:
            self.play_bt.setIcon(QIcon(Func.getImage("operate/play.png")))

    # 设置可选参数
    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    def updateInfo(self):
        self.pro_window.updateInfo()

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties)

    def loadSetting(self):
        self.pro_window.loadSetting()

    def getProperties(self, display=True) -> dict:
        """
        get this widget's properties to show it in Properties Window.
        @return: a dict of properties
        """
        self.refresh()
        return self.pro_window.getProperties()

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        self.updateInfo()
        return self.default_properties

    def restore(self, properties: dict):
        self.setProperties(properties)

    def clone(self, new_widget_id: str, new_widget_name):
        self.updateInfo()
        clone_widget = SoundDisplay(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties)
        clone_widget.apply()
        return clone_widget

    # 返回各项参数
    # 大部分以字符串返回，少数点击选择按钮返回布尔值
    # 因为有些地方引用Attribute
    def getFilename(self) -> str:
        """
        返回图片文件名（relative path）
        :return:
        """
        return self.default_properties.get("General").get("File Name")

    def getBufferSize(self) -> str:
        """
        返回Buffer Size(ms)
        :return:
        """
        return self.pro_window.general.buffer_size.text()

    def getRefillMode(self) -> str:
        """
        返回Refill Mode
        :return:
        """
        return self.pro_window.general.stream_refill.currentText()

    def getStartOffset(self) -> str:
        """
        返回Start Offset
        :return:
        """
        return self.pro_window.general.start_offset.text()

    def getStopOffset(self) -> str:
        """
        返回Stop Offset
        :return:
        """
        return self.pro_window.general.stop_offset.text()

    def getRepetitions(self) -> str:
        """
        返回Loop
        :return:
        """
        return self.pro_window.general.repetitions.text()

    def getIsVolumeControl(self) -> bool:
        """
        返回音量控制
        :return:
        """
        return bool(self.pro_window.general.volume_control.checkState())

    def getSyncToVbl(self) -> bool:
        """
        返回音量控制
        :return:
        """
        return bool(self.pro_window.general.sync_to_vbl.checkState())

    def getVolume(self) -> str:
        """
        返回音量
        :return:
        """
        return self.pro_window.general.volume.text()

    def getClearAfter(self) -> str:
        """
        返回是否clear after
        :return:
        """
        return self.pro_window.general.clear_after.currentText()

    def getScreenName(self) -> str:
        """
        返回Screen Name
        :return:
        """
        return self.pro_window.general.screen_name.currentText()

    def getSoundDeviceName(self) -> str:
        """
        返回 sound device name
        :return:
        """
        return self.pro_window.general.sound.currentText()

    def getIsLatencyBias(self) -> bool:
        """
        返回Pan控制
        :return:
        """
        return bool(self.pro_window.general.latency_bias.checkState())

    def getBiasTime(self) -> str:
        """
        返回pan
        :return:
        """
        return self.pro_window.general.bias_time.text()

    def getWaitForStart(self) -> str:
        """
        返回 wait_for_start
        :return:
        """
        return self.pro_window.general.wait_for_start.currentText()

    def getDuration(self) -> str:
        """
        返回duration
        :return:
        """
        return self.pro_window.duration.duration.currentText()

    def getOutputDevice(self) -> dict:
        """
        返回输出设备
        :return:
        """
        return self.pro_window.duration.default_properties.get("Output Devices", {})

    def getInputDevice(self) -> dict:
        """
        返回输入设备
        :return: 输入设备字典
        """
        return self.pro_window.duration.default_properties.get("Input Devices", {})

