from app.func import Func
from app.info import Info
from lib import DockWidget
from .properties_table import PropertiesTable


class Properties(DockWidget):
    """
    This widget is used to output information about states of software.
    """

    def __init__(self):
        super(Properties, self).__init__()
        # title
        self.setWindowTitle("Properties")
        # properties table
        self.properties_table = PropertiesTable()
        self.setWidget(self.properties_table)
        # current widget id
        self.current_widget_id = Info.ERROR_WIDGET_ID

    def showProperties(self, widget_id: str):
        """
        show widget's properties
        :param widget_id:
        :return:
        """
        # we should clear firstly
        self.clear()
        # add
        self.current_widget_id = widget_id
        properties = Func.getWidgetProperties(widget_id, display=True)
        # sorted_properties = sorted(properties.items(), key=lambda x: x[0])
        # for key, value in sorted_properties:
        #     self.properties_table.addProperty(key, str(value))
        # no sorting!!!
        for key, value in properties.items():
            self.properties_table.addProperty(key, str(value))

    def clear(self):
        """
        show widget's properties
        :return:
        """
        self.properties_table.setRowCount(0)
