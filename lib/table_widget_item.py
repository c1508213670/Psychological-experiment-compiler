from PyQt5.QtWidgets import QTableWidgetItem


class TableWidgetItem(QTableWidgetItem):
    """

    """

    def __init__(self, value: str = ""):
        super(TableWidgetItem, self).__init__(value)
        # save old current_text to redo
        if value:
            self.old_text = value
        else:
            self.old_text = ""

    def redo(self):
        """
        redo its current_text, you should combine it with func save()
        :return:
        """
        self.setText(self.old_text)

    def save(self):
        """

        :return:
        """
        self.old_text = self.text()

    def setText(self, p_str):
        """

        :param p_str:
        :return:
        """
        self.old_text = p_str
        super(TableWidgetItem, self).setText(p_str)

    def changed(self):
        """

        :return:
        """
        return self.old_text != self.text()
