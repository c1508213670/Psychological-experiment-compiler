import numpy as np
import qimage2ndarray
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem

from app.func import Func
from app.info import Info
from .gabor import GaborProperty
from .snow import SnowProperty


class OtherItem(QGraphicsPixmapItem):
    Snow, Gabor = 10, 11
    name = {
        Snow: Info.ITEM_SNOW,
        Gabor: Info.ITEM_GABOR,
    }

    def __init__(self, item_type, item_name: str = ""):
        super(OtherItem, self).__init__()

        self.item_type = item_type
        self.item_name = item_name if item_name else self.generateItemName()

        if self.item_type == OtherItem.Snow:
            self.pro_window = SnowProperty()
            self.setPixmap(QPixmap(Func.getImage("widgets/Snow.png")).scaled(100, 100))
        elif self.item_type == OtherItem.Gabor:
            self.pro_window = GaborProperty()
            self.setPixmap(QPixmap(Func.getImage("widgets/Gabor.png")).scaled(100, 100))

        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.properties = self.pro_window.default_properties
        self.default_properties = {
            'Name': self.item_name,
            'Z': self.zValue(),
            'X': 1,
            'Y': 1,
            "Properties": self.properties
        }

    def mouseDoubleClickEvent(self, event):
        self.openPro()

    def setAttributes(self, attributes):
        self.pro_window.setAttributes(attributes)

    def generateItemName(self) -> str:
        name = self.name[self.item_type]
        cnt = Info.COMBO_COUNT.get(name)
        item_name = f"{name}_{cnt}"
        Info.COMBO_COUNT[name] += 1
        return item_name

    def openPro(self):
        self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setPosition()
        self.setWh()
        self.pro_window.show()

    def getName(self):
        return self.item_name

    def ok(self):
        self.apply()
        self.pro_window.close()

    def cancel(self):
        self.pro_window.loadSetting()

    def apply(self):
        self.updateInfo()
        self.changeSomething()

    def updateInfo(self):
        self.pro_window.updateInfo()
        self.default_properties["X"] = self.scenePos().x()
        self.default_properties["Y"] = self.scenePos().y()
        self.default_properties["Z"] = self.zValue()

    def getInfo(self):
        self.updateInfo()
        return self.default_properties

    def changeSomething(self):
        # print(f"rect: {self.boundingRect()}")
        # __w = self.properties["Width"]
        # w = int(__w) if __w.isdigit() else self.boundingRect().width()
        # __h = self.properties["Height"]
        # h = int(__h) if __h.isdigit() else self.boundingRect().height()

        # __cx = self.properties["Center X"]
        # cx = int(__cx) if __cx.isdigit() else self.getUnRotatedScenePos().x() + w/2
        # __cy = self.properties["Center Y"]
        # cy = int(__cy) if __cy.isdigit() else self.getUnRotatedScenePos().y() + h/2
        w, _ = self.getItemPos(self.properties["Width"], True, True)
        h, _ = self.getItemPos(self.properties["Height"], False, True)
        # positions
        cx, isRef = self.getItemPos(self.properties["Center X"], True)
        cx = cx + w/2 if isRef else cx

        cy, isRef = self.getItemPos(self.properties["Center Y"], False)
        cy = cy + h/2 if isRef else cy

        __rotate = self.properties["Rotation"]
        rotate = round(float(__rotate), 2) if __rotate.isdigit() else 0

        if self.item_type == self.Snow:
            __scale = self.properties["Scale"]
            scale = int(__scale) if __scale.isdigit() else 8

            __transparency = self.properties['Transparency']

            if __transparency.endswith("%"):
                cTransValue = int(__transparency[0:-1])/100
            elif __transparency.startswith(["["]):
                cTransValue = 1
            else:
                cTransValue = int(__transparency)

            cTransValue = max(cTransValue, 0)
            cTransValue = min(cTransValue, 1)

            snow_stimulate = self.getSnow(h // scale, w // scale)
            pix = QPixmap(qimage2ndarray.array2qimage(snow_stimulate))

            new_pix = QPixmap(pix.size())
            new_pix.fill(Qt.transparent)

            painter = QPainter(new_pix)
            painter.setOpacity(cTransValue)
            painter.drawPixmap(QPoint(), pix)
            painter.end()

            self.setPixmap(new_pix.scaled(w, h))
            # self.setPixmap(pix.scaled(w, h))

        elif self.item_type == self.Gabor:
            __spatial = self.properties['Spatial']
            spatial = 0.033 if __spatial.startswith("[") else float(__spatial)

            __contrast = self.properties['Contrast']
            contrast = 1 if __contrast.startswith("[") else float(__contrast)

            __phase = self.properties['Phase']
            phase = 0 if __phase.startswith("[") else float(__phase)

            __orientation = self.properties['Orientation']
            orientation = 0 if __orientation.startswith("[") else float(__orientation)

            __back_color = self.properties['Back Color']
            back_color = (128.0, 128.0, 128.0) if __back_color.startswith("[") else tuple(
                float(x) for x in __back_color.split(","))

            __sdx = self.properties['SDx']
            sdx = 30 if __sdx.startswith("[") else int(__sdx)

            __sdy = self.properties['SDy']
            sdy = 30 if __sdy.startswith("[") else int(__sdy)

            __transparency = self.properties['Transparency']

            if __transparency.endswith("%"):
                cTransValue = int(__transparency[0:-1])/100
            elif __transparency.startswith(["["]):
                cTransValue = 1
            else:
                cTransValue = int(__transparency)

            cTransValue = max(cTransValue, 0)
            cTransValue = min(cTransValue, 1)

            gabor_stim = self.getGabor(spatial, contrast, phase, orientation, back_color, w, h, sdx, sdy)
            pix = QPixmap(qimage2ndarray.array2qimage(gabor_stim))

            new_pix = QPixmap(pix.size())
            new_pix.fill(Qt.transparent)

            painter = QPainter(new_pix)
            painter.setOpacity(cTransValue)
            painter.drawPixmap(QPoint(), pix)
            painter.end()

            # self.setPixmap(pix.scaled(w, h, Qt.KeepAspectRatio))
            self.setPixmap(new_pix.scaled(w, h, Qt.KeepAspectRatio))

        # print(f"cx: {cx}, cy: {cy}, w/2: {w/2},h/2: {h/2}")
        self.setPos(QPoint(cx - (w / 2), cy - (h / 2)))
        # self.setPos(QPoint(cx, cy))

        x = self.boundingRect().center().x()
        y = self.boundingRect().center().y()

        self.setTransformOriginPoint(x, y)
        self.setRotation(rotate)
        self.update()

    @staticmethod
    def getSnow(h, w, is_binary = False):
        snow = np.random.rand(int(h), int(w))
        if is_binary:
            snow[snow <= 0.5] = 0
            snow[snow > 0.5] = 255
        else:
            snow = snow * 255
        snow.astype(np.uint8)
        return snow

    @staticmethod
    def getGabor(cycles_per_pix, contrast, phase, orientation, back_color: tuple, width, height, sdx, sdy):
        phase = (phase % 360) * (np.pi / 180)
        orientation = (orientation % 360) * (np.pi / 180)
        # to force the width and height to be even
        width = int(width / 2.0) * 2
        height = int(height / 2.0) * 2

        radius = (int(width / 2.0), int(height / 2.0))
        [x, y] = np.meshgrid(range(-radius[0], radius[0] + 1), range(-radius[1], radius[1] + 1))

        circle_mask = (x / radius[0]) ** 2 + (y / radius[1]) ** 2

        circle_mask = circle_mask >= 1

        # xm = x * np.cos(orientation) - y * np.sin(orientation)
        # ym = x * np.sin(orientation) + y * np.cos(orientation)

        # xm = x * np.cos(orientation) - y * np.sin(orientation)
        # ym = x * np.sin(orientation) + y * np.cos(orientation)

        circular_gaussian_mask_matrix = np.exp(-((x / sdx) ** 2 + (y / sdy) ** 2) / 2)
        circular_gaussian_mask_matrix[circle_mask] = 0

        f = 2 * np.pi * cycles_per_pix
        a = np.cos(orientation) * f
        b = np.sin(orientation) * f

        layer = 255 * circular_gaussian_mask_matrix * (np.cos(a * x + b * y + phase) * contrast + 1.0) / 2.0

        gabor = np.zeros((height + 1, width + 1, 3))

        for i in range(height + 1):
            for j in range(width + 1):
                for k in range(3):
                    gabor[i, j, k] = layer[i, j]

        for iDim in range(0, np.size(back_color)):
            gabor[:, :, iDim] = gabor[:, :, iDim] + (1 - circular_gaussian_mask_matrix) * back_color[iDim]

        gabor.astype(np.uint8)
        return gabor

    def setPosition(self):
        un_rotated_scene_pos = self.getUnRotatedScenePos()

        width = self.boundingRect().width()
        height = self.boundingRect().height()

        self.pro_window.setPosition(un_rotated_scene_pos.x() + (width / 2), un_rotated_scene_pos.y() + (height / 2))

    def setWh(self):
        w = self.boundingRect().width()
        h = self.boundingRect().height()

        self.pro_window.setWh(w, h)

    def getUnRotatedScenePos(self):
        rotate = self.rotation()
        if rotate != 0:
            self.setRotation(0)
            un_rotated_scene_pos = self.scenePos()
            self.setRotation(rotate)
        else:
            un_rotated_scene_pos = self.scenePos()
        return un_rotated_scene_pos

    def setProperties(self, properties: dict):
        self.pro_window.setProperties(properties.get("Properties"))
        self.default_properties["X"] = properties["X"]
        self.default_properties["Y"] = properties["Y"]
        self.default_properties["Z"] = properties["Z"]
        self.loadSetting()

    def loadSetting(self):
        x = self.default_properties.get("X", 0)
        y = self.default_properties.get("Y", 0)
        z = self.default_properties.get("Z", 0)
        self.setPos(x, y)
        self.setZValue(z)

    def clone(self):
        self.updateInfo()
        new = OtherItem(self.item_type)
        new.setProperties(self.default_properties.copy())
        new.changeSomething()
        return new

    def setZValue(self, z: float) -> None:
        self.default_properties["Z"] = z
        super(OtherItem, self).setZValue(z)

    def getItemPos(self, posStr, isX: bool = True, isWH: bool = False, decNum: int = 0):
        """
        :param posStr:
        :param isX:  is x or y
        :param isWH: is width and height or center XY
        :param decNum:
        :return:
        """
        # __w = self.properties["Width"]
        # w = int(__w) if __w.isdigit() else self.boundingRect().width()
        # __h = self.properties["Height"]
        # h = int(__h) if __h.isdigit() else self.boundingRect().height()
        #
        # __cx = self.properties["Center X"]
        # cx = int(__cx) if __cx.isdigit() else self.getUnRotatedScenePos().x() + w/2
        # __cy = self.properties["Center Y"]
        # cy = int(__cy) if __cy.isdigit() else self.getUnRotatedScenePos().y() + h/2

        isRef = False

        if isinstance(posStr, str):
            if Func.isPercentStr(posStr):
                # percent
                if isX:
                    posStr = round(float(posStr[0:-1]) * self.scene().width() / 100, decNum)
                else:
                    posStr = round(float(posStr[0:-1]) * self.scene().height() / 100, decNum)
            elif posStr.isdigit():
                # digit
                posStr = round(float(posStr), decNum)
            else:
                # all others: ref
                isRef = True
                if isWH:
                    if isX:
                        posStr = self.boundingRect().width()
                    else:
                        posStr = self.boundingRect().height()
                else:
                    if isX:
                        posStr = self.getUnRotatedScenePos().x()
                    else:
                        posStr = self.getUnRotatedScenePos().y()

        return posStr, isRef