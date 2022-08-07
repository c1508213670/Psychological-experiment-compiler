from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from app.func import Func
from app.info import Info
from lib import TabWidget


class Center(QMainWindow):
    """

    """
    # when current widget change, emit this to refresh. (widget_id)
    currentWidgetChanged = pyqtSignal(str)

    def __init__(self):
        super(Center, self).__init__()
        self.setObjectName("Center")
        # set tab widget as its main widget
        self.tab_widget = TabWidget()
        self.setCentralWidget(self.tab_widget)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """
        link necessary signals
        """
        self.tab_widget.currentChanged.connect(self.handleTabChange)

    def openTab(self, widget_id: str):
        """
        open widget as tab according to its widget_id
        """
        # open widget as a tab in tab widget
        # this widget may have been opened in tab widget
        widget_type = Func.getWidgetType(widget_id)
        widget = Info.Widgets[widget_id]

        if widget_type == Info.IF:
            widget.condition_area.loadSetting()
        elif widget_type == Info.SWITCH:
            widget.case_area.loadSetting()
        # elif widget_type == Info.QUEST_UPDATE:
        #     widget.loadSetting()

        self.tab_widget.openTab(widget, widget_type, widget.widget_name)

    def closeTab(self, widget_id: str) -> None:
        """
        close widget in tab widget
        @param widget_id:
        @return:
        """
        widget = Info.Widgets[widget_id]
        self.tab_widget.closeTab(widget)

    def changeTabName(self, widget_id: str, widget_name: str) -> None:
        """
        if widget's was changed, its tab name should be changed as well.
        @param widget_id:
        @param widget_name: new widget's name
        @return:
        """
        widget = Info.Widgets[widget_id]
        self.tab_widget.changeTabName(widget, widget_name)

    def handleTabChange(self, index: int):
        """
        when tab current tab change, we need to emit signal to refresh other docks.
        @param index:
        @return:
        """
        # if close all tab, index will be -1
        if index != -1:
            # emit currentWidgetChanged signal to refresh other docks.
            widget = self.tab_widget.widget(index)
            self.currentWidgetChanged.emit(widget.widget_id)
        else:
            self.currentWidgetChanged.emit(Info.ERROR_WIDGET_ID)

    def store(self) -> list:
        """
        store some opening widgets' widget_id
        :return:
        """
        return self.tab_widget.store()

    def restore(self, data: list):
        """
        restore some opening widgets
        :return:
        """
        self.tab_widget.restore(data)

    def clear(self):
        """
        close all tabs
        :return:
        """
        self.tab_widget.clear()
