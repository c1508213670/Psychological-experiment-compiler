import copy
import os
import re
import subprocess
import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDesktopWidget

from app.info import Info


class Func(object):
    """
    This class stores some common functions
    """
    ############################
    # determination of str type
    ############################
    @staticmethod
    def isPercentStr(inputStr):
        if isinstance(inputStr, str):
            return re.fullmatch(r"^\d*(\.\d+)?%$", inputStr)
        return False
    ############################
    # update device information
    ############################
    @staticmethod
    def getDeviceInfo(device_type: str) -> dict:
        """
        for each widget which has device information such as screen or sound.
        :param device_type: screen or sound, and maybe more in the future.
        :return:
        """
        devices = {}
        for k, v in {**Info.OUTPUT_DEVICE_INFO, **Info.QUEST_DEVICE_INFO, **Info.TRACKER_DEVICE_INFO}.items():
            if k.startswith(device_type):
                devices[k] = v["Device Name"]
        #
        # if device_type == "quest" and len(devices) > 1:
        #     devices["quest_rand"] = "quest_rand"
        return devices

    @staticmethod
    def getDeviceNameById(device_id: str) -> str:
        for k, v in {**Info.OUTPUT_DEVICE_INFO, **Info.INPUT_DEVICE_INFO}.items():
            if device_id == k:
                return v.get("Device Name")
        return ""

    @staticmethod
    def getCurrentScreenColor(screen_id: str) -> str:
        if screen_id == "":
            return "255,255,255"

        return Info.OUTPUT_DEVICE_INFO[screen_id].get("Back Color", "255,255,255")

    @staticmethod
    def getCurrentScreenRes(screen_id: str, need_color: bool = False) -> tuple:
        if screen_id == "":
            if need_color:
                return 640, 480, "255,255,255"
            else:
                return 640, 480
        resolution = Info.OUTPUT_DEVICE_INFO[screen_id].get('Resolution', "auto")
        wh = resolution.lower().split('x')

        if len(wh) > 1:
            width = int(wh[0])
            height = int(wh[1])
        else:
            scr_rect = QDesktopWidget().screenGeometry()
            width = scr_rect.width()
            height = scr_rect.height()
        if need_color:
            color = Info.OUTPUT_DEVICE_INFO[screen_id].get("Back Color", "255,255,255")
            return width, height, color
        else:
            return width, height

    ###########################################
    #           compile version func              #
    ###########################################
    @staticmethod
    def getImage(image_name: str) -> str:
        """
        返回指定name的图片路径
        :param image_name:
        :return:
        """
        return os.path.join(Info.ImagePath, *(re.split(r'[\\/]', image_name)))

    @staticmethod
    def getImageForStyleSheet(image_name: str) -> str:
        """
        返回指定name的图片路径
        :param image_name:
        :return:
        """
        cImage_path = Func.getImage(image_name)
        return "/".join(re.split(r'[\\/]', cImage_path))

    @staticmethod
    def getWidgetPosition(widget_id: str) -> int:
        return Func.getWidgetIndex(widget_id)

    @staticmethod
    def getNextWidgetId(widget_id: str) -> str:
        """
        得到附近下一个widget的wid, 如果要查询的widget_id是末尾或者不存在，返回None
        :param widget_id:
        :return:
        """
        # 如果是widget是timeline，不存在位置信息
        if Func.isWidgetType(widget_id, Info.TIMELINE):
            return Info.ERROR_WIDGET_ID
        #
        try:
            node = Info.WID_NODE[widget_id]
            parent_node = node.parent()
            # if node is if/switch's child node
            if Func.isWidgetType(parent_node.widget_id, Info.IF) or Func.isWidgetType(parent_node.widget_id,
                                                                                      Info.SWITCH):
                node = parent_node
                parent_node = node.parent()
            index = parent_node.indexOfChild(node)
            try:
                return parent_node.child(index + 1).widget_id
            except:
                return Info.ERROR_WIDGET_ID
        except:
            return Info.ERROR_WIDGET_ID

    @staticmethod
    def getPreviousWidgetId(widget_id: str) -> str:
        """
        得到附近前一个widget的wid, 如果要查询的widget_id是末尾或者不存在，返回None
        :param widget_id:
        :return:
        """
        # 如果是widget是timeline，不存在位置信息
        if Func.isWidgetType(widget_id, Info.TIMELINE):
            return Info.ERROR_WIDGET_ID
        #
        try:
            node = Info.WID_NODE[widget_id]
            parent_node = node.parent()
            # if node is if/switch's child node
            if Func.isWidgetType(parent_node.widget_id, Info.IF) or Func.isWidgetType(parent_node.widget_id,
                                                                                      Info.SWITCH):
                node = parent_node
                parent_node = node.parent()
            index = parent_node.indexOfChild(node)
            try:
                return parent_node.child(index - 1).widget_id
            except:
                return Info.ERROR_WIDGET_ID
        except:
            return Info.ERROR_WIDGET_ID

    @staticmethod
    def getWidgetIDInTimeline(widget_id: str) -> list:
        """
        得到一个timeline中所有的widget的widget_id的list，按顺序放置
        :param widget_id: timeline的widget_id
        :return:
        """
        return Func.getWidgetChildren(widget_id)

    @staticmethod
    def isWidgetType(widget_id: str, widget_type: str):
        """
        根据输入的widget_id来判断是不是输入的类型
        :param widget_id: 需要判断的id
        :param widget_type: 需要确定的类型
        :return:
        """
        try:
            return widget_id.split('.')[0] == widget_type
        except:
            return False

    @staticmethod
    def getParentWid(widget_id: str) -> str:
        return Func.getWidgetParent(widget_id)

    @staticmethod
    def getWidLevel(widget_id: str) -> int:
        """
        通过输入的wid得到该widget所在层级，从0开始累加，即最初始的timeline为0，往后递增
        :param widget_id: 输入的wid
        :return: 如果wid不存在，返回-1
        """
        try:
            node = Info.WID_NODE[widget_id]
        except:
            return -1
        # 不断迭代，直至父结点为空
        level = 0
        node = node.parent()
        while node:
            node = node.parent()
            level += 1
        return level

    @staticmethod
    def getWidgetsTotalLayer(widget_id: str = f"{Info.TIMELINE}.0") -> int:
        """
        返回最大level，深度优先遍历
        :return:
        """
        node = Info.WID_NODE[widget_id]
        max_child_count = 0
        for i in range(node.childCount()):
            temp_count = Func.getWidgetsTotalLayer(node.widget_id)
            if temp_count > max_child_count:
                max_child_count = temp_count
        return 1 + max_child_count

    ###########################################
    #           new version func              #
    ###########################################
    @staticmethod
    def isLinuxRetinalScr() -> bool:
        return Info.IS_RETINA_SCR_LINUX
        # isRetinal = False
        #
        # if Info.OS_TYPE == 2:
        #     if Info.IS_RETINA_SCR_LINUX == -1:
        #         cmdOut = subprocess.run("xdpyinfo | grep dots", shell=True, capture_output=True).stdout
        #         s = re.findall(r' (\d+)x(\d+) dots per inch', cmdOut.decode(sys.stdout.encoding))
        #
        #         for iScreen in s:
        #             for ixy in iScreen:
        #                 if int(ixy) > 100:
        #                     Info.IS_RETINA_SCR_LINUX = 1
        #                     return True
        #     else:
        #         return Info.IS_RETINA_SCR_LINUX > 0
        # else:
        #     return False
        #
        # return isRetinal

    @staticmethod
    def getWidget(widget_id: str):
        """
        get widget through its widget id
        """
        return Info.Widgets[widget_id]

    @staticmethod
    def getNode(widget_id: str):
        """
        get node through its widget id
        """
        return Info.Nodes[widget_id]

    @staticmethod
    def generateWidgetId(widget_type: str) -> str:
        """
        generate a valid widget id
        """
        count = Info.WidgetTypeCount[widget_type]
        widget_id = f"{widget_type}.{count}"
        Info.WidgetTypeCount[widget_type] += 1
        return widget_id

    @staticmethod
    def generateWidgetName(widget_type: str) -> str:
        """
        generate a valid widget name
        """
        while True:
            # widget name = 'widget_type' _ 'count'
            widget_name = f"{widget_type}_{Info.WidgetNameCount[widget_type]}"
            # inc count of this widget type
            Info.WidgetNameCount[widget_type] += 1
            # check name's validity
            if widget_name not in Info.Names:
                return widget_name

    @staticmethod
    def checkWidgetNameValidity(widget_name: str) -> (bool, str):
        """
        check the validity of widget name.
        It should be unique, unless it's a reference.
        """
        if not re.match(Info.WidgetPattern[0], widget_name):
            return False, Info.WidgetPattern[1]
        if widget_name in Info.Names:
            return False, "Name already exists."
        elif widget_name in Info.MatlabFunNames:
            return False, "Name should not be a built-in key function name in MATLAB."
        elif widget_name in Info.PBBuiltinFunNames:
            return False, "Name should not be a built-in key function name in PsyBuilder."
        elif widget_name in Info.PtbBuiltinFunNames:
            return False, "Name should not be a built-in key function or variable name in Psychtoolbox."
        elif re.fullmatch(r'.+_APL$',widget_name):
            return False, "Name should not end with '_APL' (it's for PsyBuilder built-in sub functions only)."
        elif re.fullmatch(r'.+_cOpR$',widget_name):
            return False, "Name should not end with '_cOpR' (it's for PsyBuilder built-in variables only)."
        elif re.fullmatch(r'^iLoop_\d+', widget_name):
            return False, "Name should not match the regular expression of 'iLoop_\d+' (it's for PsyBuilder built-in variables only)."
        return True, ""

    @staticmethod
    def getFullFilePath(relativeFilePath: str) -> str:
        if not relativeFilePath:
            return relativeFilePath
        if Func.isRef(relativeFilePath) == 1:
            return relativeFilePath
        return os.path.join(Info.FILE_DIRECTORY, *(re.split(r'[\\/]', relativeFilePath)))

    @staticmethod
    def getRelativeFilePath(fullFileName: str):
        if fullFileName:
            # for full reference
            if Func.isRef(fullFileName) == 1:
                return fullFileName

            # for relative path just return
            if fullFileName[0].isalpha() and ":" not in fullFileName:
                return fullFileName

            if not Info.FILE_DIRECTORY:
                Func.printOut("The current project has not been saved yet, save it first:", 0)
                Info.Psy.saveFile()

            beSavedDir = Info.FILE_DIRECTORY

            try:
                commonPath = os.path.commonpath([fullFileName, beSavedDir])

                if len(commonPath) > 0 and re.sub(r'[\\/]', r'\\', commonPath) != re.sub(r'[\\/]', r'\\', beSavedDir):
                    raise Exception

                fullFileName = fullFileName[len(commonPath) + 1:]
            except:
                if not Func.isRef(fullFileName):
                    Func.printOut(f"All experimental materials should be put in the folder: {beSavedDir}", 3)
                    # raise Exception(f"All experimental materials (e.g., images) should be put under the folder: {beSavedDir}")
        return fullFileName

    @staticmethod
    def isRef(inputStr: str) -> int:
        """
        :param inputStr:
        :return: 0,1,2 for no ref, full, and partial reference string respectively
        """
        if not isinstance(inputStr, str):
            return 0
        # full reference string
        if inputStr.startswith('[') and inputStr.endswith(']'):
            return 1
        # partial reference string
        elif re.search(r'(\[[A-Za-z]+[a-zA-Z._0-9]*?\])', inputStr):
            return 2

        return 0


    @staticmethod
    def getWidgetType(widget_id: str):
        """
        get widget's type through its widget id
        """
        return widget_id.split('.')[0]

    @staticmethod
    def getWidgetName(widget_id: str):
        """
        get widget's name
        """
        return Info.Widgets[widget_id].widget_name

    @staticmethod
    def checkWidgetNameExisted(widget_name: str) -> bool:
        """
        check widget name whether existed
        """
        return widget_name in Info.Names

    @staticmethod
    def getWidgetReference(widget_id: str) -> list:
        """
        get list of reference widget's widget id
        @param widget_id:
        @return:
        """
        widget_name = Func.getWidgetName(widget_id)
        if widget_name not in Info.Names:
            Func.printOut(f"failed to find '{widget_name}' in Info.Names ", 2)
        return Info.Names[widget_name]

    @staticmethod
    def getWidgetParent(widget_id: str) -> str:
        """
        get parent's widget id
        @param widget_id:
        @return:
        """
        # print(widget_id)
        parentWd = Info.Nodes[widget_id].parent()
        if parentWd:
            return parentWd.widget_id
        else:
            return parentWd

    @staticmethod
    def getWidgetChild(widget_id: str, index: int) -> (str, str):
        """
        no usages
        @param widget_id:
        @param index:
        @return: child's widget id and widget name
        """
        child = Info.Nodes[widget_id].child(index)
        return child.widget_id, child.text(0)

    @staticmethod
    def getWidgetChildren(widget_id: str) -> list:
        """
        get its children
        @param widget_id:
        @return: list of children's widget id and widget name
        """
        root = Info.Nodes[widget_id]
        children = []
        for i in range(root.childCount()):
            child = root.child(i)
            children.append((child.widget_id, child.text(0)))
        return children

    @staticmethod
    def getWidgetIndex(widget_id: str) -> int:
        """
        get widget's index in timeline
        @param widget_id:
        @return:
        """
        if Func.isWidgetType(widget_id, Info.TIMELINE):
            # we ignore timeline'pos
            return -1
        node = Info.Nodes[widget_id]
        parent_node = node.parent()
        if parent_node:
            if Func.isWidgetType(parent_node.widget_id, Info.IF) or Func.isWidgetType(parent_node.widget_id,
                                                                                      Info.SWITCH):
                # if widget is child of if/switch, its pos is its parent's pos
                node = parent_node
                parent_node = node.parent()
            return parent_node.indexOfChild(node)
        else:
            return -1

    @staticmethod
    def getWidgetProperties(widget_id: str, display: bool = False) -> dict:
        """
        get widget's properties through its widget id
        """
        widget = Info.Widgets[widget_id]
        if display:
            return widget.getProperties()
        if Func.isWidgetType(widget_id, Info.TIMELINE) or Func.isWidgetType(widget_id, Info.LOOP):
            return widget.getProperties()
        dp: dict = copy.deepcopy(widget.store())

        # slider
        pro = dp.get("Properties")
        g = dp.get("General")
        if pro:
            g = pro.get("General")
            f = pro.get("Frame")
            d = pro.get("Duration")
            dp["Properties"] = {**g, **f, **d}

            new_items = {}
            items: dict = dp["Items"]
            for k, v in items.items():
                temp = copy.deepcopy(v)
                temp.update({**v["Properties"]})
                temp.pop("Properties")
                new_items[k] = temp
                # new_items[k] = {
                #     "X": v["X"],
                #     "Y": v["Y"],
                #     "Z": v["Z"],
                #     "Name": v["Name"],
                #     **v["Properties"],
                # }
            dp["Items"] = new_items
        elif g:
            f = dp.get("Frame", {})
            d = dp.get("Duration")
            dp = {**g, **f, **d}
        return dp

    @staticmethod
    def getWidgetAttributes(widget_id: str, detail: bool = False):
        """
        get widget's attributes through its widget id

        """
        attributes = {"subName": 0, "subNum": 0, "sessionNum": 0, "subGender": 0, "subHandedness": 0, "subAge": 0, "runNum": 0}

        # 添加quest设备全局参数
        if len(Info.QUEST_DEVICE_INFO.items()) > 1:
            attributes["questRandValue"] = ""
        for k, v in Info.QUEST_DEVICE_INFO.items():
            v: dict
            quest_name = v.get("Device Name")
            attributes[f"{quest_name}.cValue"] = ""

        # get widget's attributes: 1. the attributes of the items in front of it in timeline (exclude cycle).
        #                          2. parents' attributes. (only cycle)
        #                          3. first parent cycle's hidden attribute
        # get level of this widget, namely depth. It can be simplified by using DFS.
        node = Info.Nodes[widget_id]
        depth = -1
        while node:
            depth += 1
            node = node.parent()
        # do 1.
        node = Info.Nodes[widget_id]
        parent = node.parent()
        if parent and Func.isWidgetType(parent.widget_id, Info.TIMELINE):
            for i in range(parent.childCount()):
                child_node = parent.child(i)
                # until it self
                if child_node.widget_id == widget_id:
                    break
                # ignore cycle before item
                if not Func.isWidgetType(child_node.widget_id, Info.LOOP):
                    for attribute in Info.Widgets[child_node.widget_id].getHiddenAttributes():
                        attributes[f"{child_node.text(0)}.{attribute}"] = depth
        # do 2. 3.
        first = True
        node = node.parent()
        depth -= 1
        while node:
            # we just need cycle
            if Func.isWidgetType(node.widget_id, Info.LOOP):
                cycle = Info.Widgets[node.widget_id]
                cycle_name = node.text(0)
                col_attributes = cycle.getColumnAttributes()
                for attribute in col_attributes:
                    attributes[f"{cycle_name}.var.{attribute}"] = depth
                # we need first cycle's hidden attribute
                if first:
                    first_cycle_hidden_attributes = Info.Widgets[node.widget_id].getHiddenAttributes()
                    for attribute in first_cycle_hidden_attributes:
                        attributes[f"{cycle_name}.{attribute}"] = depth
                    first = False
            node = node.parent()
            depth -= 1

        # ********* untested ************
        # 是否需要详细信息
        return attributes if detail else list(attributes.keys())

    @staticmethod
    def getImageObject(image_path: str, type: int = 0, size: QSize = None) -> QPixmap or QIcon:
        """
        get image from its relative path, return qt image object, include QPixmap or QIcon.
        @param image_path: its relative path
        @param type: 0: pixmap (default),
                     1: icon
        @return: Qt image object
        """
        path = os.path.join(Info.ImagePath, *(re.split(r'[\\/]', image_path)))
        if not type:
            if size:
                return QPixmap(path).scaled(size, transformMode=Qt.SmoothTransformation)
            return QPixmap(path)
        else:
            if size:
                return QIcon(QPixmap(path).scaled(size, transformMode=Qt.SmoothTransformation))
        return QIcon(path)

    @staticmethod
    def startWait():
        """
        show loading window
        """
        Info.Psy.startWait()

    @staticmethod
    def endWait():
        """
        close loading window
        """
        Info.Psy.endWait()

    @staticmethod
    def printOut(information: str, information_type: int = 0):
        """
        print information in output.
        information_type: 0 none
                          1 success
                          2 fail
        """
        Info.Psy.output.printOut(str(information), information_type)

    @staticmethod
    def checkReferValidity(target_timeline_widget_id: str, widget_id: str) -> bool:
        """
        当从structure中拖拽至timeline时，
        :param target_timeline_widget_id: 目标的timeline的wid
        :param widget_id: 被拖拽的wid
        :return: 合法性
        """
        target_timeline_node = Info.Nodes[target_timeline_widget_id]
        widget_name = Func.getWidgetName(widget_id)
        # 先确定被拖拽的widget所属的cycle是否与target的timeline所属的cycle是否为同一个
        # target_timeline不能是第一层timeline，因为它没有父cycle
        if target_timeline_widget_id == f"{Info.TIMELINE}.0":
            return False
        cycle_1_wid = target_timeline_node.parent().widget_id
        # 根据widget得到父timeline
        parent_timeline_node = Info.Nodes[Func.getWidgetParent(widget_id)]
        # 如果是父亲为第一层timeline，其没有父cycle
        if parent_timeline_node.widget_id == f"{Info.TIMELINE}.0":
            return False
        cycle_2_wid = parent_timeline_node.parent().widget_id
        # 父cycle是否相同
        return Func.getWidgetName(cycle_1_wid) == Func.getWidgetName(cycle_2_wid)
