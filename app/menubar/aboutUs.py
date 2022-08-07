from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFontMetrics, QPixmap, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QTextEdit, QLabel, QFrame, QVBoxLayout, QHBoxLayout

from app.func import Func


class AboutUs(QWidget):
    def __init__(self, parent=None):
        super(AboutUs, self).__init__(parent=parent)

        self.setWindowTitle("About developers of PsyBuilder 0.1")
        self.setWindowModality(2)
        self.setWindowIcon(QIcon(Func.getImage("common/icon.png")))
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(QPalette.Background, Qt.white)

        cBkIm = QPixmap(Func.getImage("common/soochowUn.png"))

        # cBkIm.scaled(self.size(),Qt.ignoreAspectRation)
        # cBrush = QBrush(cBkIm.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        # # cBrush.setStyle(Qt.RadialGradientPattern)
        # p.setBrush(QPalette.Background, cBrush)

        self.setPalette(p)

        info = QTextEdit(self)
        info.setReadOnly(True)
        info.setTextInteractionFlags(Qt.NoTextInteraction)
        info.setFrameShape(QFrame.NoFrame)

        # info.setTextBackgroundColor()
        info.setHtml("<b>PsyBuilder (ver 0.1)</b> for Psychtoolbox3 under MATLAB "
                     "was developed by Prof. "
                     "<a style='color: blue;' href=\"http://web.suda.edu.cn/yzhangpsy/index.html\">Yang Zhang</a> "
                     "(Attention and Perception lab, Soochow university, Suzhou, China) and his colleagues."
                     "<br><br><b>PsyBuilder 0.1</b> is provided as is—no warranty is made or implied by "
                     "the authors of the software, or by anyone else. This software "
                     "is designed for research purposes only, not to be used for "
                     "any business purpose, such as, but not limited to, business training."
                     )

        cP = info.palette()
        cP.setColor(QPalette.Base,QColor(255,255,255,0))
        info.setPalette(cP)

        info.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        info.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        info.setFixedHeight(QFontMetrics(info.font()).lineSpacing() * 11)

        author1 = self.getInfo("authorInfo01",
                               "Yang Zhang (张阳), Ph.D., Prof.<br>Department of Psychology, Soochow University, Suzhou"
                               "<br><a href='mailto:yzhangpsy@suda.edu.cn?Subject= Inquire about the usage of PsyBuilder 0.1'>yzhangpsy@suda.edu.cn</a>")
        author2 = self.getInfo("authorInfo02", "Zhe Yang, Ph.D., Associate Prof. <br> Department of computer science, Soochow University, Suzhou")

        author3 = self.getInfo("authorInfo03", "Chenzhi Feng, Ph.D., Prof. <br> Department of Psychology, Soochow University, Suzhou")

        author4 = self.getInfo("authorInfo_zhicheng", "Zhicheng Lin, Ph.D., Prof. <br> Applied Psychology,  Chinese University of Hong Kong, Shenzhen")
        layout = QVBoxLayout()
        layout.addWidget(info, 2)
        layout.addLayout(author1, 1)
        layout.addLayout(author2, 1)
        layout.addLayout(author3, 1)
        layout.addLayout(author4, 1)

        self.setLayout(layout)

    def getInfo(self, name: str, info: str):
        head_portrait = QLabel()
        head_portrait.setFixedSize(QSize(100, 100))
        detail = QLabel()
        head_portrait.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        detail.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        head_portrait.setPixmap(QPixmap(Func.getImage(f"authors/{name}.png")))
        detail.setTextFormat(Qt.RichText)
        detail.setTextInteractionFlags(Qt.TextBrowserInteraction)
        detail.setOpenExternalLinks(True)
        detail.setText(info)

        layout = QHBoxLayout()
        layout.addWidget(head_portrait, stretch=0)
        layout.addWidget(detail, stretch=1)
        return layout
