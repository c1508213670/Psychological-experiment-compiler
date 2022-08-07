from lib import TableWidgetItem


class RepetitionsItem(TableWidgetItem):
    def __init__(self, value: str):
        super(RepetitionsItem, self).__init__(value)
        # a flag
        self.new = True
        self.pattern = r"^[0-9]+$"
