from PyQt5.QtCore import Qt, QUrl, QFileInfo, pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QKeyEvent
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QToolBar, QAction, QLabel, QSizePolicy, QStackedWidget

from app.func import Func
from lib import MessageBox, TabItemMainWindow
from .videoProperty import VideoProperty


class VideoDisplay(TabItemMainWindow):
    def __init__(self, widget_id: str, widget_name: str):
        super(VideoDisplay, self).__init__(widget_id, widget_name)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.mediaStatusChanged.connect(self.loadStatue)
        self.video_widget = VideoWidget()

        self.mediaPlayer.setVideoOutput(self.video_widget)

        self.mediaPlayer.positionChanged.connect(self.stopPlaying)
        self.mediaPlayer.stateChanged.connect(self.changeIcon)

        self.label = QLabel()
        self.pro_window = VideoProperty()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.label)
        self.stack.addWidget(self.video_widget)

        self.default_properties = self.pro_window.default_properties

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.file: str = ""
        self.start_pos = 0
        self.end_pos = 9999999
        self.playback_rate = 1.0
        self.aspect_ration_mode = -1

        self.setUI()

    def setUI(self):
        self.setWindowTitle("Video")
        self.label.setText("Your video will appear here")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # self.setCentralWidget(self.label)
        self.setCentralWidget(self.stack)
        self.stack.setCurrentIndex(0)


        tool = QToolBar()
        open_pro = QAction(QIcon(Func.getImage("menu/setting.png")), "setting", self)
        open_pro.triggered.connect(self.openSettingWindow)
        tool.addAction(open_pro)

        self.play_video = QAction(QIcon(Func.getImage("operate/start_video.png")), "start", self)
        self.play_video.triggered.connect(self.playVideo)
        tool.addAction(self.play_video)
        self.video_widget.play_and_pause.connect(lambda: self.play_video.trigger())

        self.addToolBar(Qt.TopToolBarArea, tool)

    def refresh(self):
        self.pro_window.refresh()
        self.setScrBackgroundColor()

    def playVideo(self):
        if self.file:
            # ????????????
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            # ?????????????????????
            else:
                self.mediaPlayer.play()
        else:
            MessageBox.warning(self, "No Video Error", "Please load video first!", MessageBox.Ok)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.parseProperties()
        file_name = self.pro_window.general.file_name.text()
        file_name = Func.getFullFilePath(file_name)
        if Func.isRef(file_name):
            file_name = ""
            self.file = ""
        if file_name:
            # self.setCentralWidget(self.video_widget)
            self.stack.setCurrentIndex(1)
            if QFileInfo(file_name).isFile():
                # ?????????????????????????????????????????????
                if file_name != self.file:
                    self.file = file_name
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))
                self.mediaPlayer.setPosition(self.getStartTime(self.start_pos))
                self.video_widget.setAspectRatioMode(self.aspect_ration_mode)
                self.mediaPlayer.setPlaybackRate(self.playback_rate)
            else:
                self.pro_window.close()
                MessageBox.warning(self, "Warning", "The file path is invalid!")
        else:
            # self.setCentralWidget(self.label)
            self.stack.setCurrentIndex(0)
        # ????????????
        self.propertiesChanged.emit(self.widget_id)

        self.setScrBackgroundColor()

    def parseProperties(self):
        self.start_pos = self.getStartTime(self.default_properties.get("Start position", "00:00:00.000"))
        self.end_pos = self.getStartTime(self.default_properties.get("End position", "99:99:99.999"))
        self.playback_rate = float(self.default_properties.get("Playback rate", "1"))
        self.aspect_ration_mode = self.default_properties.get("Aspect ratio", "Default")
        if self.aspect_ration_mode == "Default":
            self.aspect_ration_mode = -1
        elif self.aspect_ration_mode == "Ignore":
            self.aspect_ration_mode = 0
        elif self.aspect_ration_mode == "Keep":
            self.aspect_ration_mode = 1
        elif self.aspect_ration_mode == "KeepByExpanding":
            self.aspect_ration_mode = 2

    # ????????????
    def loadStatue(self, media_statue):
        """
        UnknownMediaStatus, NoMedia, LoadingMedia, LoadedMedia, StalledMedia,
        BufferingMedia, BufferedMedia, EndOfMedia, InvalidMedia
        """
        # ???????????????
        if media_statue == QMediaPlayer.UnknownMediaStatus:
            self.play_video.setEnabled(False)
            # self.setCentralWidget(label)
            self.play_video.setText("Unknown Media")  # self.statusBar().showMessage("Unknown Media", 5000)

        # ?????????
        elif media_statue == QMediaPlayer.NoMedia:
            self.play_video.setEnabled(False)
            self.play_video.setText("No Media")
        # ?????????
        elif media_statue == QMediaPlayer.LoadingMedia:
            self.play_video.setEnabled(False)
            self.play_video.setText("Loading Media")
        # ????????????
        elif media_statue == QMediaPlayer.LoadedMedia:
            self.play_video.setEnabled(True)
            self.play_video.setText("Start")
        # ????????????
        elif media_statue == QMediaPlayer.StalledMedia:
            pass
        # ?????????
        elif media_statue == QMediaPlayer.BufferingMedia:
            pass
        # ????????????
        elif media_statue == QMediaPlayer.BufferedMedia:
            pass
        # ????????????
        elif media_statue == QMediaPlayer.EndOfMedia:
            pass
        # ????????????
        elif media_statue == QMediaPlayer.InvalidMedia:
            self.play_video.setEnabled(False)
            self.play_video.setText("Invalid Media")

    @staticmethod
    def getStartTime(str_time):
        try:
            h = int(str_time[0:2])
            m = int(str_time[3:5])
            s = int(str_time[6:8])
            x = int(str_time[9:12])
            return h * 60 * 60 * 1000 + m * 60 * 1000 + s * 1000 + x
        except ValueError:
            return 0
        except Exception as e:
            return 0

    def setScrBackgroundColor(self):
        # if not sip.isdeleted(self.label):
        color = Func.getCurrentScreenColor(self.pro_window.getScreenId())
        self.label.setStyleSheet("background-color: rgb({});".format(color))

    def setVideo(self):
        # self.setCentralWidget(self.video_widget)
        self.stack.setCurrentIndex(1)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.file)))

        self.mediaPlayer.setPosition(self.getStartTime(self.start_pos))
        self.video_widget.setAspectRatioMode(self.aspect_ration_mode)

    def stopPlaying(self, duration):
        if abs(self.end_pos - duration) < 1000:
            self.mediaPlayer.pause()

    def changeIcon(self, statue):
        if statue == QMediaPlayer.PlayingState:
            self.play_video.setIcon(QIcon(Func.getImage("operate/pause_video.png")))
            self.play_video.setText("pause")
        else:
            self.play_video.setIcon(QIcon(Func.getImage("operate/start_video.png")))
            self.play_video.setText("start")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            self.play_video.trigger()
            event.accept()
        else:
            super(VideoDisplay, self).keyPressEvent(event)

    def setAttributes(self, attributes):
        format_attributes = ["[{}]".format(attribute) for attribute in attributes]
        self.pro_window.setAttributes(format_attributes)

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties)
        self.apply()

    def updateInfo(self):
        self.pro_window.updateInfo()

    def loadSetting(self):
        self.pro_window.setProperties(self.default_properties)

    # ??????????????????
    # ?????????????????????????????????????????????????????????????????????
    # ????????????????????????Attribute
    def getFilename(self) -> str:
        """
        ????????????????????????relative path???
        :return:
        """
        return self.default_properties.get("General").get("File Name")

    def getStartPosition(self) -> str:
        """
        ?????????????????????hh:mm:ss.xxx???
        :return:
        """
        return self.pro_window.general.start_pos.text()

    def getEndPosition(self) -> str:
        """
        ?????????????????????hh:mm:ss.xxx???
        :return:
        """
        return self.pro_window.general.end_pos.text()

    def getPlaybackRate(self) -> str:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.general.playback_rate.currentText()

    def getAspectRatio(self) -> str:
        """
        ????????????????????????
        :return:
        """
        return self.pro_window.general.aspect_ratio.currentText()

    def getScreenName(self) -> str:
        """
        ??????Screen Name
        :return:
        """
        return self.pro_window.general.screen_name.currentText()

    def getIsClearAfter(self) -> str:
        """
        ????????????clear after
        :return:
        """
        return self.pro_window.general.clear_after.currentText()

    def getXAxisCoordinates(self) -> str:
        """
        ??????x?????????
        :return:
        """
        return self.pro_window.frame.x_pos.currentText()

    def getYAxisCoordinates(self) -> str:
        """
        ??????y?????????
        :return:
        """
        return self.pro_window.frame.y_pos.currentText()

    def getWidth(self) -> str:
        """
        ????????????
        :return:
        """
        return self.pro_window.frame.width.currentText()

    def getHeight(self) -> str:
        """
        ????????????
        :return:
        """
        return self.pro_window.frame.height.currentText()

    def getEnable(self) -> str:
        """
        ??????frame enable
        :return:
        """
        return self.pro_window.frame.enable.currentText()

    def getFrameTransparent(self) -> str:
        """??????frame transparent"""
        return self.pro_window.frame.transparent.text()

    def getBorderColor(self) -> str:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.frame.dot_color.currentText()

    def getBorderWidth(self) -> str:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.frame.border_width.currentText()

    def getFrameBackColor(self) -> str:
        """
        ?????????????????????
        :return:
        """
        return self.pro_window.frame.back_color.getRGB()

    def getDuration(self) -> str:
        """
        ??????duration
        :return:
        """
        return self.pro_window.duration.duration.currentText()

    def getOutputDevice(self) -> dict:
        """
        ??????????????????
        :return:
        """
        return self.pro_window.duration.default_properties.get("Output Devices", {})

    def getInputDevice(self) -> dict:
        """
        ??????????????????
        :return: ??????????????????
        """
        return self.pro_window.duration.default_properties.get("Input Devices", {})

    """
    Functions that must be complete in new version
    """

    def getProperties(self) -> dict:
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
        clone_widget = VideoDisplay(new_widget_id, new_widget_name)
        clone_widget.setProperties(self.default_properties.copy())
        clone_widget.apply()
        return clone_widget


# ??????????????????
class VideoWidget(QVideoWidget):
    play_and_pause = pyqtSignal()

    def __init__(self, parent=None):
        super(VideoWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.setAttribute(Qt.WA_OpaquePaintEvent, True)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            self.play_and_pause.emit()
        # esc????????????
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.setFullScreen(False)
            event.accept()
        # ??????????????????Alt+Enter?????????????????????
        elif event.key() == Qt.Key_Enter and event.modifiers() == Qt.Key_Alt:
            self.setFullScreen(not self.isFullScreen())
            event.accept()
        else:
            super(VideoWidget, self).keyPressEvent(event)

    # ????????????????????????
    def mouseDoubleClickEvent(self, event):
        self.setFullScreen(not self.isFullScreen())
        event.accept()
