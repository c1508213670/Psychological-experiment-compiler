from PyQt5.QtCore import pyqtSignal, QSize, Qt

from app.func import Func
from app.info import Info
from lib import TabItemMainWindow
from .loop_table import CycleTable
from .properties import Properties


class Loop(TabItemMainWindow):
    # when add new timeline, emit signal(parent_widget_id, widget_id, widget_name, index)
    itemAdded = pyqtSignal(str, str, str, int)
    # when delete signals, emit signal(sender_widget, widget_id)
    itemDeleted = pyqtSignal(int, str)

    def __init__(self, widget_id: str, widget_name: str):
        super(Loop, self).__init__(widget_id, widget_name)
        self.cycle_table = CycleTable()
        self.properties = Properties()
        self.setCentralWidget(self.cycle_table)
        # set tool bar
        self.setToolBar()
        # init one row
        self.cycle_table.addRow(0)
        # link signals
        self.linkSignals()

    def linkSignals(self):
        """
        link signals
        """
        self.cycle_table.timelineAdded.connect(
            lambda widget_id, widget_name, index: self.itemAdded.emit(self.widget_id, widget_id, widget_name, index))
        self.cycle_table.timelineDeleted.connect(lambda widget_id: self.itemDeleted.emit(Info.CycleSend, widget_id))
        self.properties.propertiesChanged.connect(lambda: self.propertiesChanged.emit(self.widget_id))

    def setToolBar(self):
        """

        @return:
        """
        tool_bar = self.addToolBar("Tool Bar")
        tool_bar.setObjectName("CycleToolBar")
        tool_bar.setMovable(False)
        tool_bar.setFloatable(False)
        # add action
        tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # settingIcon = Func.getImageObject("cycle/setting.png", 1, QSize(22, 22))

        IconSize = QSize(22,22)

        tool_bar.addAction(Func.getImageObject("cycle/setting.png", 1,  IconSize), "Setting", self.properties.exec)
        tool_bar.addAction(Func.getImageObject("cycle/add_row.png", 1, IconSize), "Add a Row", self.addRow)
        tool_bar.addAction(Func.getImageObject("cycle/add_rows.png", 1, IconSize), "Add Rows",
                           self.cycle_table.addRowsActionFunc)
        tool_bar.addAction(Func.getImageObject("cycle/delete_row.png", 1, IconSize), "Delete Rows",
                           self.cycle_table.deleteRowsActionFunc)
        tool_bar.addAction(Func.getImageObject("cycle/add_column.png", 1, IconSize), "Add a Variable",
                           self.cycle_table.addAttributeActionFunc)
        tool_bar.addAction(Func.getImageObject("cycle/add_columns.png", 1, IconSize), "Add Variables",
                           self.cycle_table.addAttributesActionFunc)
        tool_bar.addAction(Func.getImageObject("cycle/delete_column.png", 1, IconSize), "Delete Variables",
                           self.cycle_table.deleteAttributesActionFunc)

    def getColumnAttributes(self) -> list:
        """
        return [attr1, attr2]
        @return:
        """
        # get column attributes
        return self.cycle_table.attributes[2:]

    def deleteTimeline(self, timeline: str):
        """

        @param timeline:
        @return:
        """
        self.cycle_table.deleteTimeline(timeline)

    def addRow(self):
        """

        @return:
        """
        self.cycle_table.addRow()

    def deleteRow(self, row: int):
        """
        delete row
        """
        self.cycle_table.deleteRow(row)

    def deleteAttribute(self, col: int):
        """
        delete attribute
        """
        self.cycle_table.deleteAttribute(col)

    def renameItem(self, old_widget_name: str, new_widget_name: str):
        """
        rename timeline
        """
        self.cycle_table.renameItem(old_widget_name, new_widget_name)

    """
    API
    """

    def rowCount(self) -> int:
        """
        返回table共有多少行
        :return:
        """
        return self.cycle_table.rowCount()

    def columnCount(self) -> int:
        """
        返回table共有多少列
        :return:
        """
        return self.cycle_table.columnCount()

    def getTimelines(self) -> list:
        """
        按顺序进行返回所有设置的timeline
        格式为 [ [timeline_name, timeline_widget_id], [], ... ]
        如果某行为空则改行对应的数据为[ '', '']
        :return:
        """
        cTimelines = []
        for row in range(0, self.cycle_table.rowCount()):
            timeline_name = self.cycle_table.item(row, 1).text()
            if timeline_name:
                cTimelines.append([timeline_name, self.cycle_table.timelines.setdefault(timeline_name, "")[0]])
            else:
                raise Exception(f"Timeline name should not be empty!:In {self.widget_name} at row {row + 1}")
        return cTimelines

    def getAttributes(self, row: int) -> dict:
        """
        return the current row of attributes
        at format of { attribute_name : attribute_value }
        如果属性值未填写则为 ''
        :param row: inquired row number
        :return:
        """
        attributes = {}

        for col in range(0, self.cycle_table.columnCount()):
            attribute_name = self.cycle_table.attributes[col]
            attributes[attribute_name] = self.cycle_table.item(row, col).text()
        return attributes

    def getAttributeValues(self, col: int) -> list:
        """
        通过输入的列索引，返回该列对应的attribute的所有value的一个列表
        :param col: 列缩影s
        :return: value的list
        """
        # col有效
        if col < 0 or col >= self.cycle_table.columnCount():
            raise Exception("invalid col index.")
        #
        values = []
        # 遍历每行，将值取出
        for row in range(self.cycle_table.rowCount()):
            values.append(self.cycle_table.item(row, col).text())
        return values

    def getOrder(self) -> str:
        """
        得到设置界面中order的值
        :return:
        """
        return self.getProperties()["order_combo"]

    def getNoRepeatAfter(self) -> str:
        """
        如上类推
        :return:
        """
        return self.getProperties()["no_repeat_after"]

    def getOrderBy(self):
        """
        如上类推
        :return:
        """
        return self.getProperties()["order_by_combo"]

    """
    Functions that must be complete in new version
    """

    def getProperties(self) -> dict:
        """
        get this widget's properties to show it in Properties Window.
        @return: a dict of properties
        """
        return self.properties.getProperties()

    def getHiddenAttributes(self) -> list:
        """
        every widget has global attributes and own attributes,
        we get global attributes through common function Func.getWidgetAttributes(widget_id) and
        we get widget's own attributes through this function.
        @return: dict of attributes
        """
        return ["cLoop", "rowNums"]

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        return {"cycle_table": self.cycle_table.store(), "properties": self.properties.getProperties()}

    def restore(self, data):
        """
        restore this widget according to data.
        @param data: necessary data for restoring this widget
        @return:
        """
        self.cycle_table.restore(data["cycle_table"])
        self.properties.setProperties(data["properties"])
