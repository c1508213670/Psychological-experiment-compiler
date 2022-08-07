from PyQt5.QtCore import Qt

from app.func import Func
from lib import TableWidgetItem


class TimelineNameItem(TableWidgetItem):
    """

    """

    def __init__(self, widget_type: str, widget_id: str, widget_name: str = ""):
        super(TimelineNameItem, self).__init__(widget_name)
        # set data, we assure widget type and widget id is valid
        self.widget_id = widget_id
        # widget name may be none, we should generate new one
        if not widget_name:
            widget_name = Func.generateWidgetName(widget_type)
        # set widget name
        self.setText(widget_name)
        # set its align
        self.setTextAlignment(Qt.AlignCenter)
