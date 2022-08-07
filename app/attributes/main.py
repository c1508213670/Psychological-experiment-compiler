from app.func import Func
from app.info import Info
from lib import DockWidget
from .attributes_table import AttributesTable


class Attributes(DockWidget):
    """
    To show widget's attributes
    """

    def __init__(self):
        super(Attributes, self).__init__()
        # title
        self.setWindowTitle("Variables")
        # attributes table
        self.attributes_table = AttributesTable()
        self.setWidget(self.attributes_table)
        # current widget id
        self.current_widget_id = Info.ERROR_WIDGET_ID

    def showAttributes(self, widget_id: str):
        """
        show widget's attributes
        """
        # we should clear firstly
        self.clear()
        # add
        self.current_widget_id = widget_id
        attributes: list = Func.getWidgetAttributes(widget_id)
        for attribute in attributes:
            self.attributes_table.addAttribute(attribute)

    def clear(self):
        """
        clear table
        """
        self.attributes_table.setRowCount(0)

    def refresh(self):
        self.showAttributes(self.current_widget_id)
