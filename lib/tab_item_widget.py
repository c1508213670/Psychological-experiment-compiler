from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from app.func import Func


class TabItemWidget(QWidget):
    """
    base class for widgets which will be tab in tab widget

    you should complete all necessary function.
    """

    """
    signals
    """

    # you can show properties in Properties Window through this signal. (widget_id)
    propertiesChanged = pyqtSignal(str)
    tabClosed = pyqtSignal(str)
    # you can show loading dialog window through this signal
    waitStart = pyqtSignal()
    # you can end loading dialog window through this signal
    waitEnd = pyqtSignal()

    def __init__(self, widget_id: str, widget_name: str):
        super(TabItemWidget, self).__init__()
        self.setWindowIcon(Func.getImageObject("common/con.png", type=1))
        # widget_id is used to distinguish different widgets
        self.widget_id = widget_id
        self.widget_name = widget_name
    """
    about properties and attributes
    """

    def getProperties(self) -> dict:
        """
        You should finish the job.

        get this widget's properties to show it in Properties Window.
        :return: a dict of properties
        """
        return {}

    def getUsingDeviceCount(self) -> int:
        """
        You should finish the job.

        return count of using device
        :return:
        :rtype:
        """
        return 0

    def getHiddenAttributes(self) -> list:
        """
        You should finish the job.
        every widget has global attributes and own attributes,
        we get global attributes through common function Func.getWidgetAttributes(widget_id) and
        we get widget's own attributes through this function.
        Its values are also depended on device whether used.
        used:
        not used:
        :return: list of attributes
        """
        if self.getUsingDeviceCount():
            return ["acc", "resp", "rt", "respOnsetTime"]
        return []

    def getUsingAttributes(self):
        using_attributes: list = []
        self.findAttributes(self.default_properties, using_attributes)
        return using_attributes

    def findAttributes(self, properties: dict, using_attributes: list):
        for v in properties.values():
            if isinstance(v, dict):
                self.findAttributes(v, using_attributes)
            elif isinstance(v, str):
                if v.startswith("[") and v.endswith("]"):
                    using_attributes.append(v[1:-1])

    """
    about widget
    """

    def store(self):
        """
        You should finish the job.

        return necessary data for restoring this widget.
        :return:
        """
        return {}

    def restore(self, data) -> None:
        """
        You should finish the job.

        restore this widget according to data.
        :param data: necessary data for restoring this widget
        :return:
        """

    def clone(self, new_widget_id: str, new_widget_name: str):
        """
        You should finish the job.

        return a copy of this widget, and set the widget id and name of the copy.
        :param widget_id:
        :return:
        """
        return None

    def changeWidgetId(self, widget_id: str):
        """
        change this widget's widget id, because referable widget may be deleted and we
        need to change widget id.
        :param widget_id:
        :return:
        """
        self.widget_id = widget_id

    """
    other function may be needed to all, but I forget those.
    """

    def __repr__(self):
        return f"{Func.getWidgetType(self.widget_id)} [{self.widget_id}: {self.widget_name}]"
