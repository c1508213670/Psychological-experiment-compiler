from PyQt5.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTableWidgetItem, QFrame, QLabel, QAbstractItemView, QMenu, QShortcut

from app.func import Func
from app.info import Info
from lib import MessageBox, TableWidget
from .timeline_item import TimelineItem
from .timeline_name_item import TimelineNameItem


class TimelineTable(TableWidget):
    """
    table to place timeline item and timeline name item
    """

    # timeline initial length of arrow
    InitialArrowLength = 10
    Height = 100
    # if Info.OS_TYPE == 2:
    if Info.IS_RETINA_SCR_LINUX:
        Width = 200
        line_height = 50
    else:
        Width = 100
        line_height = 25

    #
    top_row = 0
    item_row = 1
    arrow_row = 2
    name_row = 3

    # item clicked and double clicked (widget_id)
    itemClicked = pyqtSignal(str)
    itemDoubleClicked = pyqtSignal(str)
    # when widget's name is changed, emit this signal (widget id, widget_name)
    itemNameChanged = pyqtSignal(str, str)
    itemDeleted = pyqtSignal(str)

    def __init__(self):
        super(TimelineTable, self).__init__(None)
        # set its qss id
        self.setObjectName("TimelineTable")
        # hide its scroll bar
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setAutoScroll(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        # hide its grid lines
        self.setFrameStyle(QFrame.NoFrame)
        self.setShowGrid(False)
        # init table
        self.initTable()
        # data
        self.item_count = 0
        # link signals
        self.linkSignals()
        # set menu and shortcut
        self.setMenuAndShortcut()

        self.setWindowIcon(Func.getImageObject("common/icon.png", 1))

    def linkSignals(self):
        """
        link signals
        @return:
        """
        self.itemChanged.connect(self.handleItemChanged)

    def setMenuAndShortcut(self):
        """
        set menu and shortcut
        @return:
        """
        self.menu = QMenu()
        # copy action
        self.delete_action = self.menu.addAction(Func.getImageObject("menu/delete.png", 1), "Delete",
                                                 self.deleteActionFunc,
                                                 QKeySequence(QKeySequence.Delete))
        # shortcut
        self.delete_shortcut = QShortcut(QKeySequence(QKeySequence("Delete")), self)
        self.delete_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.delete_shortcut.activated.connect(self.deleteActionFunc)
        self.backspace_shortcut = QShortcut(QKeySequence(QKeySequence("Backspace")), self)
        self.backspace_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.backspace_shortcut.activated.connect(self.deleteActionFunc)

    def contextMenuEvent(self, e):
        """

        @param e:
        @return:
        """
        col = self.columnAt(e.pos().x())
        row = self.rowAt(e.pos().y())
        if row == self.item_row and col <= self.item_count:
            if self.cellWidget(row, col):
                self.menu.exec(self.mapToGlobal(e.pos()))

    def deleteActionFunc(self):
        """

        @return:
        """
        try:
            if self.selectedIndexes():
                row = self.selectedIndexes()[0].row()
                col = self.selectedIndexes()[0].column()
                widget_id = self.cellWidget(row, col).widget_id
                # emit signal
                self.itemDeleted.emit(widget_id)
                # delete column
                self.deleteItem(widget_id)
        except:
            pass

    def initTable(self):
        """
        init table: 1. arrow
                    2. three row
        @return:
        """
        # 5 rows and 10 columns
        self.setRowCount(4)
        self.setRowHeight(self.item_row, TimelineTable.Height)
        self.setColumnCount(10)
        # set initial arrow
        for col in range(TimelineTable.InitialArrowLength - 1):
            self.setUnselectableItem(self.top_row, col)
            self.setUnselectableItem(self.item_row, col)
            self.setArrow(col, "timeline/line.png")
            self.setUnselectableItem(self.name_row, col)
        self.setUnselectableItem(self.top_row, TimelineTable.InitialArrowLength - 1)
        self.setUnselectableItem(self.item_row, TimelineTable.InitialArrowLength - 1)
        self.setArrow(TimelineTable.InitialArrowLength - 1, "timeline/arrow.png", 50)
        self.setUnselectableItem(self.name_row, TimelineTable.InitialArrowLength - 1)

    def setUnselectableItem(self, row: int, col: int):
        """
        set unselectable item in table
        @param row:
        @param col:
        @return:
        """
        item = QTableWidgetItem("")
        item.setFlags(Qt.ItemIsEnabled)
        self.setItem(row, col, item)

    def setArrow(self, col: int, image_path: str, width: int = Width, height: int = line_height):
        """
        set arrow pixmap in table
        @param image_path:
        @return:
        """
        # set column width
        self.setColumnWidth(col, width)
        # set pixmap
        label = QLabel()
        label.setPixmap(Func.getImageObject(image_path,0, QSize(width, height)))

        label.setFocusPolicy(Qt.NoFocus)
        label.setStyleSheet("background: white;")
        self.setCellWidget(self.arrow_row, col, label)

    def addItem(self, widget_type: str = None, widget_id: str = None, widget_name: str = None, index: int = 0) -> (
            str, str, int):
        """
        add item in timeline table
        @param timeline_item:
        @param timeline_name_item:
        @param index:
        @return: add index
        """
        # generate a timeline item and timeline name item
        timeline_item = TimelineItem(widget_type, widget_id)
        timeline_name_item = TimelineNameItem(timeline_item.widget_type, timeline_item.widget_id, widget_name)
        # link items' signals
        timeline_item.clicked.connect(lambda widget_id: self.itemClicked.emit(widget_id))
        timeline_item.doubleClicked.connect(lambda widget_id: self.itemDoubleClicked.emit(widget_id))
        # bind timeline name item to timeline item
        timeline_item.timeline_name_item = timeline_name_item
        # no matter what, insert a column first
        if index > self.item_count or index == -1:
            index = self.item_count

        # we need animation, you can cancel it.
        # self.startMoveToNextAnimation(index)

        # insert new column to add new item
        self.insertColumn(index)
        self.setArrow(index, "timeline/line.png")
        self.setUnselectableItem(self.top_row, index)
        self.setCellWidget(self.item_row, index, timeline_item)
        self.setItem(self.name_row, index, timeline_name_item)
        # change data
        self.item_count += 1
        # if initial length is not full, we should delete one column
        if self.item_count < TimelineTable.InitialArrowLength - 1:
            self.removeColumn(TimelineTable.InitialArrowLength - 2)
        return timeline_item.widget_id, timeline_name_item.text(), index

    def deleteItem(self, widget_id: str):
        """
        delete item in timeline table
        @param widget_id:
        @return:
        """
        # find index of widget_id
        index = self.itemIndexByWidgetId(widget_id)
        # delete
        if index != -1:
            # if item count is greater than the initial length, we should delete arrow line
            if self.item_count <= TimelineTable.InitialArrowLength - 2:
                self.insertColumn(TimelineTable.InitialArrowLength - 2)
                self.setUnselectableItem(self.top_row, TimelineTable.InitialArrowLength - 2)
                self.setUnselectableItem(self.item_row, TimelineTable.InitialArrowLength - 2)
                self.setArrow(TimelineTable.InitialArrowLength - 2, "timeline/line.png")
                self.setUnselectableItem(self.name_row, TimelineTable.InitialArrowLength - 2)
            self.removeColumn(index)
            # change data
            self.item_count -= 1

    def moveItem(self, origin_index: int, dest_index: int) -> (str, int):
        """
        move item
        return widget id and index
        """
        widget_id = self.cellWidget(self.item_row, origin_index).widget_id
        widget_name = self.item(self.name_row, origin_index).text()
        # delete old
        self.deleteItem(widget_id)
        if origin_index < dest_index:
            dest_index -= 1
        # add new
        _, _, dest_index = self.addItem(widget_id=widget_id, widget_name=widget_name, index=dest_index)
        return widget_id, dest_index

    def renameItem(self, origin_widget_name: str, new_widget_name: str):
        """
        change item's name.
        @param origin_widget_name:
        @param new_widget_name:
        @return:
        """
        for col in range(self.item_count):
            item = self.item(self.name_row, col)
            if item.text() == origin_widget_name:
                item.setText(new_widget_name)
                break

    def itemIndexByWidgetId(self, widget_id: str) -> int:
        """
        find item's col according to its widget id
        @param widget_id:
        @return:
        """
        for col in range(self.item_count):
            if widget_id == self.cellWidget(self.item_row, col).widget_id:
                return col
        return -1

    def itemIndexByWidgetName(self, widget_name: str) -> int:
        """
        if item or its reference exist in this timeline, return its index, else -1
        @param widget_id:
        @return:
        """
        for col in range(self.item_count):
            if widget_name == self.item(self.name_row, col).text():
                return col
        return -1

    def itemWidgetIdByWidgetName(self, widget_name: str):
        """

        @param widget_name:
        @return:
        """
        for col in range(self.item_count):
            widget = self.item(self.name_row, col)
            if widget_name == widget.text():
                return widget.widget_id
        return -1

    def itemWidgetIdByIndex(self, index: int):
        """

        @param index:
        @return:
        """
        try:
            return self.cellWidget(self.item_row, index).widget_id
        except:
            return Info.ERROR_WIDGET_ID

    def itemWidgetNameByIndex(self, index: int):
        try:
            return self.item(self.name_row, index).text()
        except:
            return ""

    def startItemAnimation(self, x: int):
        """
        show items' animation according to horizontal coordinate
        @param x: horizontal coordinate
        @return:
        """
        # get the column corresponding to the x coordinate
        col = self.columnAt(x)
        # show frame_animation according to col
        if self.item_count:
            # if excel the range, col will be -1
            if col == -1 or col >= self.item_count:
                # all items left
                for i in range(self.item_count):
                    self.startAlignmentAnimation(i, 0)
            else:
                # we need judge mouse in left or right half
                if self.columnAt(x + 50) == col:
                    # in the left half
                    for i in range(col):
                        self.startAlignmentAnimation(i, 0)
                    for i in range(col, self.item_count):
                        self.startAlignmentAnimation(i, 1)
                else:
                    # in the right half
                    for i in range(col + 1):
                        self.startAlignmentAnimation(i, 0)
                    for i in range(col + 1, self.item_count):
                        self.startAlignmentAnimation(i, 1)

    def startAlignmentAnimation(self, col: int, direction: int = 0):
        """
        set alignment of item in table in form of animation
        @param col:
        @param direction: 0. left
                          1. right
        @return:
        """
        widget: TimelineItem = self.cellWidget(self.item_row, col)
        if direction:
            # right
            x = TimelineTable.Width - TimelineItem.IconSize
            y = (TimelineTable.Height - TimelineItem.IconSize) / 2
        else:
            # left
            x = 0
            y = (TimelineTable.Height - TimelineItem.IconSize) / 2
        frame_rect = QRect(x, y, TimelineItem.IconSize, TimelineItem.IconSize)
        widget.startFrameAnimation(frame_rect, direction)

    def resetAlignmentAnimation(self):
        """
        reset alignment of item in table in form of animation
        @return:
        """
        # reset alignment
        for col in range(self.item_count):
            widget: TimelineItem = self.cellWidget(self.item_row, col)
            x = (TimelineTable.Width - TimelineItem.IconSize) / 2
            y = (TimelineTable.Height - TimelineItem.IconSize) / 2
            frame_rect = QRect(x, y, TimelineItem.IconSize, TimelineItem.IconSize)
            widget.startFrameAnimation(frame_rect)

    def startMoveToNextAnimation(self, start_col: int):
        """
        too many bugs.
        move to next pos animation and it starts form col provided.
        @return:
        """
        for col in range(start_col, self.item_count):
            widget: TimelineItem = self.cellWidget(self.item_row, col)
            geometry = widget.geometry()
            x = geometry.x() + TimelineTable.Width
            y = geometry.y()
            width = geometry.width()
            height = geometry.height()
            rect = QRect(x, y, width, height)
            widget.startGeometryAnimation(rect)

    def startMoveToPreAnimation(self, start_col: int):
        """
        too many bugs.
        move to pre pos animation and it starts form col provided.
        @return:
        """
        for col in range(start_col, self.item_count):
            widget: TimelineItem = self.cellWidget(self.item_row, col)
            geometry = widget.geometry()
            x = geometry.x() - TimelineTable.Width
            y = geometry.y()
            width = geometry.width()
            height = geometry.height()
            rect = QRect(x, y, width, height)
            widget.startGeometryAnimation(rect)

    def mouseDestIndex(self, x: int, widget_name: str = ""):
        """
        get the index pointed by the mouse according to the x coordinate
        """
        col = self.columnAt(x)
        if col >= self.item_count or col == -1:
            return self.item_count
        direction = self.cellWidget(self.item_row, col).direction
        if direction == 0:
            # left
            if widget_name == self.item(self.name_row, col).text():
                return col
            return col + 1
        else:
            # right
            if col == 0:
                return col
            else:
                if widget_name == self.item(self.name_row, col - 1).text():
                    return col - 1
                return col

    def handleItemChanged(self, item):
        """
        when cell changed, we need to make judgement
        @param item:
        @return:
        """
        # we just deal this type
        if type(item) == TimelineNameItem:
            # if text isn't changed, we ignore it
            if item.changed():
                # check its validity
                validity, tip = Func.checkWidgetNameValidity(item.text())
                if validity:
                    self.itemNameChanged.emit(item.widget_id, item.text())
                    item.save()
                else:
                    MessageBox.information(self, "warning", tip)
                    item.redo()

    def store(self):
        """
        return necessary data for restoring this widget.
        @return:
        """
        table_data = []
        for col in range(self.item_count):
            widget_id = self.cellWidget(self.item_row, col).widget_id
            widget_name = self.item(self.name_row, col).text()
            table_data.append([widget_id, widget_name])
        return {"table_data": table_data}

    def restore(self, data: dict):
        """
        restore this widget according to data.
        @param data: necessary data for restoring this widget
        @return:
        """
        table_data = data["table_data"]
        for widget_id, widget_name in table_data:
            self.addItem(widget_id=widget_id, widget_name=widget_name, index=-1)
