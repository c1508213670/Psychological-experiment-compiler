from PyQt5.QtWidgets import QDialog

from app.func import Func


class Dialog(QDialog):
    """
    not using.
    """

    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        # set its icon
        self.setWindowIcon(Func.getImageObject("common/icon.png", type=1))
