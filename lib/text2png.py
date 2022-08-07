import io
import sys

import numpy as np
import scipy.io as sio
from PIL import Image as PillIma
from PyQt5.QtCore import Qt, QBuffer
from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtWidgets import QGraphicsTextItem, QApplication


class Text2Png(QGraphicsTextItem):
    def __init__(self):
        super(Text2Png, self).__init__()
        self.setPlainText('Hello World')
        # font = QFont()
        # font.setPointSize(20)  # set the initial font size to 20 pt (dot)
        # self.setFont(font)
        #
        # bkColor = '0,0,0,0'
        # foreColor = '255,128,96'
        # transparency = '100%'
        # content = 'testtest'
        # html = f'<body style = "font-size: {23}pt;">\
        #                         <p style = "background-color: rgba({bkColor})">\
        #                         <font style = "color: rgba({foreColor},{transparency})">\
        #                          {content}</font></p></body>'
        # font = self.font()
        # font.setPointSize(23)
        #
        # self.setFont(font)
        #
        # self.setHtml(html)


    def export2Png(self, fullFilename: str, isPNG: bool = False) -> bool:
        scrPixmap = QPixmap(self.boundingRect().size().toSize())
        scrPixmap.fill(Qt.transparent)

        cPainter = QPainter(scrPixmap)
        cPainter.setRenderHint(QPainter.Antialiasing, True)

        self.document().drawContents(cPainter)

        cPainter.end()

        # save to png
        if isPNG:
            scrPixmap.toImage().save(fullFilename)
        else:
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)

            scrPixmap.toImage().save(buffer, "PNG")

            pil_im = PillIma.open(io.BytesIO(buffer.data()))

            sio.savemat(fullFilename, {'data': np.asarray(pil_im)})

            buffer.close()

        return False

    def changeText(self, content:str, family: str, size: int, foreColor: str,  transparency: str, bkColor: str, style, isRight2Left: bool = False):
        if isRight2Left:
            content = content[-1::-1]

        html = f'<body style = "font-size: {size}pt; "font-family: {family}">\
                                <p style = "background-color: rgba({bkColor})">\
                                <font style = "color: rgba({foreColor},{transparency})">\
                                 {content}</font></p></body>'

        if style == "normal_0":
            style = 0
        elif style == "bold_1":
            style = 1
        elif style == "italic_2":
            style = 2
        elif style == "underline_4":
            style = 4
        elif style == "outline_8":
            style = 8
        elif style == "overline_16":
            style = 16
        elif style == "condense_32":
            style = 32
        elif style == "extend_64":
            style = 64
        else:
            style = int(style) if style.isdigit() else 0

        font = self.font()
        font.setFamily(family)
        font.setPointSize(size)
        font.setBold(style & 1)
        font.setItalic(style & 2)
        font.setUnderline(style & 4)
        font.setStrikeOut(style & 8)
        font.setOverline(style & 16)
        if style & 32:
            font.setStretch(75)  # condensed 75
        if style & 64:
            font.setStretch(125)  # expanded 125
        self.setFont(font)

        self.setHtml(html)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    v = Text2Png()
    v.export2Png('test.mat', False)

    sys.exit(app.exec_())
