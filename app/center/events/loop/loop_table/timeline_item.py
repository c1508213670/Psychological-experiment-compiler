from lib import TableWidgetItem


class TimelineItem(TableWidgetItem):
    def __init__(self):
        super(TimelineItem, self).__init__(None)
        self.pattern = r"^[a-zA-Z][a-zA-Z0-9_]*$"
