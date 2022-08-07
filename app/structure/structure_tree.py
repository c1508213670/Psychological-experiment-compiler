from PyQt5.QtCore import pyqtSignal, Qt, QDataStream, QIODevice, QByteArray, QMimeData, QPoint, QSize
from PyQt5.QtGui import QDrag, QKeySequence
from PyQt5.QtWidgets import QTreeWidget, QMenu, QShortcut

from app.func import Func
from app.info import Info
from lib import MessageBox
from .structure_node import StructureNode


class StructureTree(QTreeWidget):
    """

    """

    # when node is double clicked, emit signal (widget_id)
    itemDoubleClicked = pyqtSignal(str)
    # when node is double deleted, emit signal (widget_id)
    itemDeleted = pyqtSignal(str)
    # when node is changed, emit(widget_id, widget_name)
    itemNameChanged = pyqtSignal(str, str)

    def __init__(self):
        super(StructureTree, self).__init__(None)
        # set one column
        self.setColumnCount(1)
        # hide header
        self.setHeaderHidden(True)
        # draggable
        self.setDragEnabled(True)
        # link signals
        self.linkSignals()
        # set menu and shortcut
        self.setMenuAndShortcut()

        # set icon size
        if Info.IS_RETINA_SCR_LINUX:
            icon_size = QSize(28, 28)
        else:
            icon_size = QSize(14, 14)

        self.setIconSize(icon_size)

    def linkSignals(self):
        """
        link signals
        @return:
        """
        self.itemChanged.connect(self.handleItemChanged)

    def setMenuAndShortcut(self):
        """

        @return:
        """
        # menu
        self.menu = QMenu()
        self.delete_action = self.menu.addAction(Func.getImageObject("menu/delete.png", 1), "Delete",
                                                 self.deleteActionFunc,
                                                 QKeySequence(QKeySequence.Delete))
        self.rename_action = self.menu.addAction(Func.getImageObject("menu/rename.png", 1), "Rename",
                                                 self.renameActionFunc,
                                                 QKeySequence("F2"))
        # shortcut
        self.rename_shortcut = QShortcut(QKeySequence('F2'), self)
        self.rename_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.rename_shortcut.activated.connect(self.renameActionFunc)
        self.delete_shortcut = QShortcut(QKeySequence("Delete"), self)
        self.delete_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.delete_shortcut.activated.connect(self.deleteActionFunc)
        self.backspace_shortcut = QShortcut(QKeySequence("Backspace"), self)
        self.backspace_shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        self.backspace_shortcut.activated.connect(self.deleteActionFunc)

    def contextMenuEvent(self, e):
        """

        @param e:
        @return:
        """
        item = self.currentItem()
        if item and item.widget_id != f"{Info.TIMELINE}.{0}":
            self.rename_action.setEnabled(True)
            self.delete_action.setEnabled(True)
            self.menu.exec(self.mapToGlobal(e.pos()))

    def addNode(self, parent_widget_id: str, widget_id: str, widget_name: str, index: int, show=True):
        """
        add node to its self
        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @param index:
        @return:
        """
        # if it has parent node
        if parent_widget_id != Info.ERROR_WIDGET_ID:
            parent_node: StructureNode = Info.Nodes[parent_widget_id]
            node = StructureNode(parent=parent_node, widget_id=widget_id)

            if Func.getWidgetType(parent_widget_id) in [Info.IF, Info.SWITCH]:
                show = False

            node.setHidden(not show)
            node.setText(0, widget_name)
            # add node
            if index != -1:
                parent_node.moveChild(index, node)
            # expand node to show its children
            parent_node.setExpanded(True)
        else:
            # create root node
            node: StructureNode = StructureNode(self, widget_id=widget_id)
            node.setHidden(not show)
            node.setText(0, widget_name)
            self.addTopLevelItem(node)
            self.collapseItem(node)
        # change Info.Nodes
        Info.Nodes[widget_id] = node

    def moveNode(self, widget_id: str, index: int):
        """
        move node
        @param widget_id:
        @param index:
        @return:
        """
        node = Info.Nodes[widget_id]
        parent = node.parent()
        parent.moveChild(index, node)

    def deleteNode(self, node: StructureNode):
        """

        @return:
        """
        node.parent().removeChild(node)

    def mouseDoubleClickEvent(self, e):
        """

        @param e:
        @return:
        """
        item = self.itemAt(e.pos())
        if item:
            self.itemDoubleClicked.emit(item.widget_id)

    def mouseMoveEvent(self, e):
        """
        drag node to timeline, but we can't move or copy cycle
        @param e:
        @return:
        """
        item = self.itemAt(e.pos())
        if item and not Func.isWidgetType(item.widget_id, Info.TIMELINE):
            widget_id = item.widget_id
            if e.modifiers() == Qt.ControlModifier:
                # ctrl -> copy
                if not Func.isWidgetType(widget_id, Info.LOOP):
                    self.copyDrag(widget_id)
            elif e.modifiers() == Qt.ShiftModifier:
                if not Func.isWidgetType(widget_id, Info.LOOP):
                    self.moveDrag(widget_id)
            else:
                # none -> refer
                self.referDrag(widget_id)

    def moveDrag(self, widget_id: str):
        """

        @param widget_id:
        @return:
        """
        data = QByteArray()
        stream = QDataStream(data, QIODevice.ReadWrite)
        stream.writeQString(widget_id)
        mime_data = QMimeData()
        mime_data.setData(Info.StructureMoveToTimeline, data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(12, 12))
        drag.exec()

    def copyDrag(self, widget_id: str):
        """

        @param widget_id:
        @return:
        """
        data = QByteArray()
        stream = QDataStream(data, QIODevice.ReadWrite)
        stream.writeQString(widget_id)
        mime_data = QMimeData()
        mime_data.setData(Info.StructureCopyToTimeline, data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(12, 12))
        drag.exec()

    def referDrag(self, widget_id: str):
        """

        @param widget_id:
        @return:
        """
        data = QByteArray()
        stream = QDataStream(data, QIODevice.ReadWrite)
        stream.writeQString(widget_id)
        mime_data = QMimeData()
        mime_data.setData(Info.StructureReferToTimeline, data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(12, 12))
        drag.exec()

    def handleItemChanged(self, item: StructureNode, index: int):
        """

        @return:
        """
        if item.changed():
            text = item.text(0)
            validity, tip = Func.checkWidgetNameValidity(text)
            if validity:
                self.itemNameChanged.emit(item.widget_id, item.text(0))
                item.save()

            else:
                MessageBox.information(self, "warning", tip)
                item.redo()

    def deleteActionFunc(self):
        """
        delete action
        @return:
        """
        # get current item
        item = self.currentItem()
        if type(item) == StructureNode:
            self.itemDeleted.emit(item.widget_id)

    def renameActionFunc(self):
        """

        @return:
        """
        # get current item
        item = self.currentItem()
        if type(item) == StructureNode and item.widget_id != f"{Info.TIMELINE}.{0}":
            self.editItem(item, 0)

    def getStructure(self, widget_id: str, widget_name: str):
        """
        get tree's structure (dfs)
        :param root:
        :return:
        """
        children = Func.getWidgetChildren(widget_id)
        children_tree = []
        for child_id, child_name in children:
            children_tree.append(self.getStructure(child_id, child_name))
        return [widget_id, widget_name, children_tree]

    def store(self) -> list:
        """
        return necessary data for restoring this widget.
        @return:
        """
        if self.topLevelItemCount():
            widget_id = self.topLevelItem(0).widget_id
            widget_name = self.topLevelItem(0).text(0)
            return self.getStructure(widget_id, widget_name)
        return []

    def restore(self, data: list):
        """
        restore this widget according to data.
        @param data: necessary data for restoring this widget
        @return:
        """
        if data:
            # add root node Timeline_0
            root_widget_id, root_widget_name, children = data
            self.addNode(Info.ERROR_WIDGET_ID, root_widget_id, root_widget_name, -1)
            # add children nodes
            for child_widget_id, child_widget_name, child_children in children:
                self.restoreNode(root_widget_id, child_widget_id, child_widget_name, child_children)

    def restoreNode(self, parent_widget_id: str, widget_id: str, widget_name: str, children: list):
        """
        restore node
        :param parent_widget_id:
        :param widget_id:
        :param widget_name:
        :param children:
        :return:
        """
        show = True
        if Func.isWidgetType(parent_widget_id, Info.IF) or Func.isWidgetType(parent_widget_id, Info.SWITCH):
            show = False
        # add node
        self.addNode(parent_widget_id, widget_id, widget_name, -1, show)
        # add children
        for child_widget_id, child_widget_name, child_children in children:
            self.restoreNode(widget_id, child_widget_id, child_widget_name, child_children)
